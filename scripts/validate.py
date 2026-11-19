#!/usr/bin/env python3
"""validate.py -- lint term files against docs/DATA-MODEL.md and the JSON Schema rules.

Standard library only (deliberate; see requirements.txt). Checks:

  V1  one term per file, filename == "<id>.md", slug pattern
  V2  required front-matter fields (schema "required") and status enum
  V3  themes: non-empty, drawn from data/themes.yaml
  V4  related edges: type from data/relationship-types.yaml, target must exist
      as a term (D-5: build fails on see-also / related pointing at a missing
      term), reason required unless type == "related"
  V5  contrasts-with edges are entered once (A->B) and not duplicated (B->A)
  V6  deprecated terms must point at a live replacement via replaced_by
  V7  dates are ISO (YYYY-MM-DD); date_last_changed >= date_created
  V8  ids unique; body starts with a definition paragraph (non-empty prose)

Usage: python3 scripts/validate.py content/terms [data_dir]
Exit 0 if clean, 1 otherwise.
"""
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED = ["id", "title", "themes", "status", "date_created", "date_last_changed"]
STATUS_ENUM = {"draft", "reviewed", "deprecated"}
FIELD_ORDER = ["contributors", "de", "replaced_by"]  # optional fields we special-case


DICT_KEYS = {"type", "target", "reason", "text", "label", "id", "name", "url", "role", "orcid", "affiliation"}


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_scalar(v):
    """true/false/null/number/string."""
    if v in ("true", "false"):
        return v == "true"
    if v in ("null", "~", ""):
        return None
    try:
        return int(v)
    except ValueError:
        return unquote(v)


def parse_front_matter(text):
    """Parse the YAML subset used in term files.

    Supported: top-level ``key: value`` and ``key:`` sections whose items are
    either scalars (``- value``) or flat dicts (``- k: v`` continued by
    further ``k: v`` lines at the same indent). No block scalars, anchors,
    or flow collections.
    """
    if not text.startswith("---\n"):
        raise SyntaxError("missing opening '---' front-matter fence")
    end = text.find("\n---", 3)
    if end < 0:
        raise SyntaxError("missing closing '---' front-matter fence")
    raw = [ln for ln in text[4:end].splitlines() if ln.strip() and not ln.lstrip().startswith("#")]

    fm, key, item = {}, None, None  # item: current list, or (dict) being filled
    i = 0
    while i < len(raw):
        ln = raw[i]
        indent = len(ln) - len(ln.lstrip())
        stripped = ln.strip()
        if indent == 0 and not stripped.startswith("- "):
            k, _, v = stripped.partition(":")
            if v.strip():
                fm[unquote(k)] = parse_scalar(v)
                key, item = None, None
            else:
                key, item = unquote(k), []
                fm[key] = item
            i += 1
            continue
        if stripped.startswith("- "):
            if key is None:
                raise SyntaxError(f"line {i}: list item outside a section")
            body = stripped[2:]
            k, _, v = body.partition(":")
            # gather continuation lines: deeper-indented 'k: v' pairs that are not new list items
            j = i + 1
            pairs = [(k.strip(), v.strip())] if v.strip() else []
            while j < len(raw):
                ni = len(raw[j]) - len(raw[j].lstrip())
                ns = raw[j].strip()
                if ni > indent and ":" in ns and not ns.startswith("- "):
                    pk, _, pv = ns.partition(":")
                    pairs.append((unquote(pk.strip()), pv.strip()))
                    j += 1
                else:
                    break
            if pairs and len(pairs) == 1 and k.strip() not in DICT_KEYS:
                item.append(parse_scalar(body))
            elif pairs:
                d = {}
                for pk, pv in pairs:
                    d[unquote(pk)] = parse_scalar(pv) if pv else ""
                item.append(d)
            else:
                item.append(parse_scalar(body))
            i = j
            continue
        raise SyntaxError(f"line {i}: cannot parse {stripped!r}")
    return fm


def id_list(vocab_path, default=()):
    """Extract the closed id list from a vocabulary YAML file."""
    out = list(default)
    if not vocab_path.exists():
        return out
    for line in vocab_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- id: \"?([a-z0-9-]+)\"?", line.strip())
        if m:
            out.append(m.group(1))
    return out


def check_file(path, themes, reltypes):
    errs, fm = [], None
    text = path.read_text(encoding="utf-8")
    try:
        fm = parse_front_matter(text)
    except SyntaxError as e:
        return [f"{path.name}: bad front matter: {e}"]

    def err(msg):
        errs.append(f"{path.name}: {msg}")

    if path.stem != str(fm.get("id", path.stem)):
        err(f"filename '{path.stem}.md' does not match id {fm.get('id')!r} (V1)")
    if not SLUG.match(str(fm.get("id", ""))):
        err(f"id {fm.get('id')!r} is not a slug (V1)")
    for f in REQUIRED:
        if f not in fm or fm.get(f) in (None, "", []):
            err(f"missing required field '{f}' (V2)")
    if fm.get("status") not in STATUS_ENUM:
        err(f"status {fm.get('status')!r} not in {sorted(STATUS_ENUM)} (V2)")
    if fm.get("title") and not str(fm["title"]).strip():
        err("title is empty (V2)")
    th = fm.get("themes") or []
    if not isinstance(th, list) or not th:
        err("themes: at least one theme required (V3)")
    else:
        for t in th:
            if t not in themes:
                err(f"themes: '{t}' not in data/themes.yaml (V3)")
    for f in ("date_created", "date_last_changed"):
        v = str(fm.get(f, ""))
        if v and not ISO.match(v):
            err(f"{f}: '{v}' is not YYYY-MM-DD (V7)")
    if all(ISO.match(str(fm.get(f, ""))) for f in ("date_created", "date_last_changed")):
        if str(fm["date_last_changed"]) < str(fm["date_created"]):
            err("date_last_changed earlier than date_created (V7)")

    related = fm.get("related") or []
    for e in related:
        if not isinstance(e, dict):
            err(f"related: expected entries with type/target, got {e!r} (V4)")
            continue
        et, tp = str(e.get("type", "")), str(e.get("target", ""))
        if tp and SLUG.match(tp) and tp == fm.get("id"):
            err("related: self-reference (V4)")
        if not et:
            err("related: empty target (V4)")
        if et and et not in reltypes:
            err(f"related: type '{et}' not in data/relationship-types.yaml (V4)")
        reason = str(e.get("reason", "")).strip()
        if not reason and et != "related":
            err(f"related: '{et} -> {et}' requires a reason (V4)")

    # V6 deprecated needs a live replacement (existence checked after first pass)
    if fm.get("status") == "deprecated":
        rb = fm.get("replaced_by")
        if not rb:
            err("deprecated term without replaced_by (V6)")

    # V8 body starts with a definition paragraph
    body = text
    if body.startswith("---"):
        end = body.find("\n---", 3)
        body = body[end + 4:].lstrip("\n") if end >= 0 else ""
    body = body.lstrip()
    if not body or body.startswith(("- ", "> ", "#")):
        err("body must start with the definition paragraph (V8)")
    return errs


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    termdir = Path(sys.argv[1])
    datadir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "data"
    themes = id_list(datadir / "themes.yaml")
    reltypes = id_list(datadir / "relationship-types.yaml")
    if not themes or not reltypes:
        print(f"cannot read vocabularies from {datadir}")
        return 1

    files = sorted(termdir.glob("*.md"))
    if not files:
        print(f"no .md term files in {termdir}")
        return 1

    all_errs, ids = [], {}
    for f in files:
        errs = check_file(f, themes, reltypes)
        all_errs.extend(errs)
        try:
            fm = parse_front_matter(f.read_text(encoding="utf-8"))
            tid = fm.get("id")
            if tid:
                ids.setdefault(tid, []).append(f.name)
        except SyntaxError:
            pass

    # V1 unique ids; V4 targets exist; V5 contrasts-with single entry; V6 live replacement
    for tid, names in ids.items():
        if len(names) > 1:
            all_errs.append(f"duplicate id '{tid}' in {names} (V1)")
    live = set(ids)
    for f in files:
        try:
            fm = parse_front_matter(f.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for e in fm.get("related") or []:
            if not isinstance(e, dict):
                continue
            tgt = str(e.get("target", ""))
            if tgt and tgt not in live:
                all_errs.append(f"{f.name}: related target '{tgt}' has no term file (V4, D-5 fail-hard)")
        back = {(str(e.get("target")), f.stem) for e in (fm.get("related") or [])
                if isinstance(e, dict) and str(e.get("type")) == "contrasts-with"}
        for a, b in back:
            rev = [x for x in (parse_front_matter((termdir / (a + ".md")).read_text(encoding="utf-8")).get("related") or [])
                   if isinstance(x, dict) and str(x.get("type")) == "contrasts-with" and str(x.get("target")) == b]
            if rev:
                all_errs.append(f"contrasts-with entered in both directions: {a} <-> {b} (V5)")
        if fm.get("status") == "deprecated":
            rb = str(fm.get("replaced_by") or "")
            if rb and rb not in live:
                all_errs.append(f"{f.name}: replaced_by '{rb}' has no term file (V6)")

    for e in all_errs:
        print("ERROR " + e)
    print(f"{len(files)} term files checked, {len(all_errs)} error(s)")
    return 1 if all_errs else 0


if __name__ == "__main__":
    sys.exit(main())
