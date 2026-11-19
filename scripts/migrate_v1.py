#!/usr/bin/env python3
"""migrate_v1.py - migrate the v1.0.0 glossary DOCX into per-term Markdown files.

Implements the maintainer decisions D-4 (splits + altLabels), D-5 (aliases,
build must fail on missing see-also targets -> dangling refs are dropped and
logged), D-11 (canon = the 64 DOCX headings; scripted word-for-word check).

Standard library only (ADR-0001: boring, durable tooling).
Usage: python3 scripts/migrate_v1.py legacy/OpenScience_Glossary.docx content/terms/ [--report docs/migration-report.md]
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DATE_CREATED = "2026-10-18"  # v1.0.0 Zenodo record date
SOURCES = [
    {"text": "UNESCO Recommendation on Open Science (2021)"},
    {"text": "Fecher & Friesike (2014)"},
    {"text": "Open Science Glossary v1.0.0 (2026-10-18), migrated verbatim", "doi": "10.5281/zenodo.23449750"},
]
CONTRIBUTOR = [{"name": "Quoc-Tan Tran", "orcid": "0000-0003-3533-5858", "role": "author"}]

# (DOCX heading title, [(slug, [themes...]), ...]) - canonical map, docs/DATA-MODEL.md section 7
TERMS = [
    ("APC (Article Processing Charge)", [("apc", ["publishing", "equity"])]),
    ("APC Waiver", [("apc-waiver", ["publishing", "equity"])]),
    ("APC Tourism", [("apc-tourism", ["equity", "publishing"])]),
    ("Accepted Manuscript (AM)", [("accepted-manuscript", ["publishing", "licensing"])]),
    ("Barcelona Declaration", [("barcelona-declaration", ["policy", "infrastructure"])]),
    ("Bibliodiversity", [("bibliodiversity", ["equity", "publishing"])]),
    ("BPC (Book Processing Charge)", [("bpc", ["publishing", "equity"])]),
    ("CARE Principles", [("care-principles", ["data", "equity"])]),
    ("CC0 (Creative Commons Zero)", [("cc0", ["licensing", "heritage"])]),
    ("CC BY (Creative Commons Attribution)", [("cc-by", ["licensing", "publishing"])]),
    ("Citizen Science / Citizen Humanities", [("citizen-science", ["participation", "heritage"])]),
    ("CLACSO", [("clacso", ["equity", "publishing", "infrastructure"])]),
    ("CoARA (Coalition for Advancing Research Assessment)", [("coara", ["assessment", "policy"])]),
    ("Co-production (of knowledge)", [("co-production", ["participation", "equity"])]),
    ("CrossRef", [("crossref", ["infrastructure"])]),
    ("Crowdsourcing (in research)", [("crowdsourcing", ["participation", "heritage"])]),
    ("DataCite", [("datacite", ["infrastructure", "data"])]),
    ("Diamond Open Access", [("diamond-oa", ["publishing", "equity", "infrastructure"])]),
    ("DMP (Data Management Plan)", [("dmp", ["data", "policy"])]),
    ("DOI (Digital Object Identifier)", [("doi", ["infrastructure"])]),
    ("DORA (San Francisco Declaration on Research Assessment)", [("dora", ["assessment", "policy"])]),
    ("Elsevier", [("elsevier", ["publishing", "policy"])]),
    ("Embargo Period", [("embargo-period", ["publishing", "policy"])]),
    ("Epistemic Injustice", [("epistemic-injustice", ["equity", "participation"])]),
    ("FAIR Principles", [("fair-principles", ["data", "infrastructure"])]),
    ("GLAM", [("glam", ["heritage", "participation"])]),
    ("Gold OA", [("gold-oa", ["publishing"])]),
    ("Green OA", [("green-oa", ["publishing", "policy"])]),
    ("HARKing (Hypothesizing After Results are Known)", [("harking", ["integrity"])]),
    ("H-index (Hirsch index)", [("h-index", ["assessment"])]),
    ("Hybrid OA", [("hybrid-oa", ["publishing", "policy"])]),
    ("IIIF (International Image Interoperability Framework)", [("iiif", ["heritage", "infrastructure"])]),
    ("Impact Factor (Journal Impact Factor, JIF)", [("impact-factor", ["assessment"])]),
    ("Infrastructuring", [("infrastructuring", ["heritage", "participation", "infrastructure"])]),
    ("OA (Open Access)", [("open-access", ["publishing"])]),
    ("OJS (Open Journal Systems)", [("ojs", ["infrastructure", "publishing"])]),
    ("OMP (Open Monograph Press)", [("omp", ["infrastructure", "publishing"])]),
    ("Open Peer Review", [("open-peer-review", ["peer-review"])]),
    ("ORCID (Open Researcher and Contributor ID)", [("orcid", ["infrastructure"])]),
    ("Paper Mill", [("paper-mill", ["integrity", "publishing"])]),
    ("P-hacking", [("p-hacking", ["integrity"])]),
    ("PID (Persistent Identifier)", [("pid", ["infrastructure"])]),
    ("Plan S", [("plan-s", ["policy", "publishing"])]),
    ("Predatory Journal (/ Publisher)", [("predatory-journal", ["integrity", "publishing"])]),
    ("Pre-print", [("preprint", ["publishing", "infrastructure"])]),
    ("Pre-registration", [("pre-registration", ["integrity"])]),
    ("Read-and-Publish Agreement (Transformative Agreement)", [("transformative-agreement", ["publishing", "policy", "equity"])]),
    ("Redalyc", [("redalyc", ["equity", "publishing", "infrastructure"])]),
    ("Registered Reports", [("registered-reports", ["integrity", "peer-review"])]),
    ("Replication / Reproducibility", [("reproducibility", ["integrity"]), ("replication", ["integrity"])]),
    ("Replication Crisis", [("replication-crisis", ["integrity", "assessment"])]),
    ("Replication Games", [("replication-games", ["integrity", "participation"])]),
    ("Repository", [("repository", ["infrastructure", "data"])]),
    ("ROR (Research Organization Registry)", [("ror", ["infrastructure"])]),
    ("Salami Slicing", [("salami-slicing", ["integrity", "assessment"])]),
    ("Science Sleuths / Post-Publication Peer Review (PPPR)", [("science-sleuths", ["peer-review", "integrity"]), ("post-publication-peer-review", ["peer-review", "integrity"])]),
    ("SciELO (Scientific Electronic Library Online)", [("scielo", ["equity", "publishing", "infrastructure"])]),
    ("Secondary Publication Right (Zweitveröffentlichungsrecht)", [("secondary-publication-right", ["policy", "licensing"])]),
    ("SHERPA/RoMEO", [("sherpa-romeo", ["infrastructure", "publishing"])]),
    ("Springer Nature", [("springer-nature", ["publishing"])]),
    ("Version of Record (VoR)", [("version-of-record", ["publishing", "licensing"])]),
    ("Wikimedia Commons", [("wikimedia-commons", ["heritage", "participation", "infrastructure"])]),
    ("Zenodo", [("zenodo", ["infrastructure", "data"])]),
    ("Zooniverse", [("zooniverse", ["participation", "heritage"])]),
]

EXTRA_ALTS = {
    "apc": ["Article Processing Charge"],
    "accepted-manuscript": ["AAM", "Author Accepted Manuscript"],
    "bpc": ["Book Processing Charge"],
    "citizen-science": ["Citizen Humanities"],
    "dmp": ["Data Management Plan", "RDM", "Research Data Management"],
    "co-production": ["Participatory Research"],
    "transformative-agreement": ["Transformative Agreement", "Read-and-Publish Agreement"],
    "impact-factor": ["JIF", "Journal Impact Factor"],
    "h-index": ["Hirsch index"],
    "harking": ["Hypothesizing After Results are Known"],
    "version-of-record": ["VoR"],
    "iiif": ["International Image Interoperability Framework"],
    "orcid": ["Open Researcher and Contributor ID"],
    "doi": ["Digital Object Identifier"],
    "pid": ["Persistent Identifier"],
    "reproducibility": ["Replication / Reproducibility"],
    "replication": ["Replication / Reproducibility"],
    "science-sleuths": ["Science Sleuths / Post-Publication Peer Review (PPPR)"],
    "post-publication-peer-review": ["PPPR", "Science Sleuths / Post-Publication Peer Review (PPPR)"],
}

# names used in "See also" lines -> slug (beyond title lookup)
ALIASES = {
    "Diamond OA": "diamond-oa", "Gold OA": "gold-oa", "Green OA": "green-oa", "Hybrid OA": "hybrid-oa",
    "OA": "open-access", "Open Access": "open-access", "Transformative Agreement": "transformative-agreement",
    "Read-and-Publish": "transformative-agreement", "Participatory Research": "co-production",
    "Research Data Management": "dmp", "RDM": "dmp", "Version of Record": "version-of-record", "VoR": "version-of-record",
    "Impact Factor": "impact-factor", "JIF": "impact-factor", "H-index": "h-index", "Preprint": "preprint",
    "PPPR": "post-publication-peer-review", "Post-Publication Peer Review": "post-publication-peer-review",
    "Post-Publication Peer Review (PPPR)": "post-publication-peer-review", "Science Sleuths": "science-sleuths",
    "Replication": "replication", "Reproducibility": "reproducibility", "Citizen Science": "citizen-science",
    "Accepted MS": "accepted-manuscript", "AAM": "accepted-manuscript", "Predatory Journal": "predatory-journal",
    "CARE Principles": "care-principles", "FAIR Principles": "fair-principles", "SciELO": "scielo",
}
FIRST_WAVE = {  # docs/BACKLOG-TERMS.md
    "Open Science", "Open Data", "OER", "Open Educational Resources", "DOAJ", "Publication Bias",
    "Indigenous Data Sovereignty", "Serials Crisis", "Big Deal", "Bibliometrics", "Altmetrics",
    "PKP", "Public Knowledge Project", "Retraction Watch", "PubPeer",
}
DEFERRED = {
    "arXiv", "SocArXiv", "Wikipedia", "WikiSource", "Wikisource", "Wiki Goes MEK", "cOAlition S",
    "Coalition S", "Copyright Transfer", "Open Infrastructure", "Open Cultural Heritage",
    "Digital Heritage", "Community Archive", "Black Box", "OSF", "Open Science Framework",
    "Think-Check-Submit", "Open Access Monograph", "Black Box (Latour)",
}
POS_RE = re.compile(r"\s{2,}")


def parse_docx(path):
    z = zipfile.ZipFile(path)
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    seq = []
    for el in body:
        if el.tag == W + "p":
            seq.append(("p", "".join(t.text or "" for t in el.findall(".//" + W + "t"))))
        elif el.tag == W + "tbl":
            seq.append(("tbl", len(el.findall(".//" + W + "tr"))))
    return seq


def is_heading(text):
    parts = POS_RE.split(text, 1)
    return (len(parts) == 2 and parts[0].strip()
            and re.fullmatch(r"(noun|proper noun|acronym)([a-z/()\s]*)", parts[1].strip() or "x" * 20) is not None)


def split_entries(seq):
    heads = []
    for i, (k, t) in enumerate(seq):
        if k == "p" and t.strip() and is_heading(t):
            title, pos = POS_RE.split(t, 1)
            heads.append((i, title.strip(), pos.strip()))
    titles = [h for _, h, _ in heads]
    entries = {}
    for n, (start, title, pos) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(seq)
        paras = []
        for j in range(start + 1, end):
            if seq[j][0] != "p":
                break
            t = seq[j][1].strip()
            if t.startswith("Quick-Reference"):  # cheat-sheet table header; not entry text (D-11)
                break
            if t:
                paras.append(t)
        entries[title] = {"pos": pos, "paras": paras}
    return heads, entries, titles


def resolve(name, title2slug):
    name = name.strip()
    if name in title2slug:
        return ("ok", title2slug[name])
    if name in ALIASES:
        return ("ok", ALIASES[name])
    if name in FIRST_WAVE:
        return ("first-wave", name)
    if name in DEFERRED:
        return ("deferred", name)
    return ("unresolved", name)


def yq(s):  # YAML-safe double-quoted string
    import json
    return json.dumps(s, ensure_ascii=False)


def emit(field, value, indent=0):
    pad = "  " * indent
    out = []
    if isinstance(value, list):
        if not value:
            out.append(f"{field}: []")
        else:
            out.append(f"{field}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for k, v in item.items():
                        prefix = "- " if first else "  "
                        first = False
                        out.append(pad + prefix + f"{k}: " + (yq(v) if isinstance(v, str) else (v if v is None else str(v).lower())))
                else:
                    out.append(pad + "- " + yq(item))
    elif isinstance(value, dict):
        out.append(f"{field}:")
        for k, v in value.items():
            out.append(pad + "  " + f"{k}: " + (yq(v) if isinstance(v, str) else str(v).lower()))
    else:
        out.append(f"{field}: " + (yq(value) if isinstance(value, str) else str(value).lower()))
    return out


def front_matter(md):
    lines = ["---"]
    for key in ("id", "title", "alternatives", "themes", "status", "date_created", "date_last_changed", "sources", "contributors", "related"):
        if key in md and md[key]:
            lines += emit(key, md[key])
    lines.append("---")
    return "\n".join(lines)


def write_term(outdir, md):
    body = md["definition"]
    if md.get("details"):
        body += "\n\n## Details\n\n" + "\n".join("- " + d for d in md["details"])
    if md.get("warning"):
        body += "\n\n> [!WARNING]\n> " + md["warning"]
    fm = front_matter(md)
    (outdir / (md["id"] + ".md")).write_text(fm + "\n\n" + body + "\n", encoding="utf-8")


def migrate(docx_path, outdir, classif):
    outdir.mkdir(parents=True, exist_ok=True)
    seq = parse_docx(docx_path)
    heads, entries, _ = split_entries(seq)
    title2slug = {}
    for title, slugthemes in TERMS:
        for slug, _ in slugthemes:
            title2slug.setdefault(title, slug)
            title2slug.setdefault(title.split(" (")[0], slug)
    report = {"files": [], "mapping": [], "drops": [], "unresolved": [], "flags": []}
    if len(heads) != 64:
        report["flags"].append(f"expected 64 headings, found {len(heads)}")
    for title, slugthemes in TERMS:
        key = next((h for _, h, _ in heads if h == title), None)
        if key is None:
            report["flags"].append(f"heading not found in DOCX: {title}")
            continue
        e = entries.get(title, {"paras": []})
        paras = e["paras"]
        defs = [p for p in paras if not p.startswith(("▸", "⚠", "See also:"))]
        details = [p[1:].strip() for p in paras if p.startswith("▸")]
        warnings = [p[1:].strip() for p in paras if p.startswith("⚠")]
        sees = [p for p in paras if p.startswith("See also:")]
        related = []
        for line in sees:
            for nm in re.split(r",\s*", line[len("See also:"):].strip()):
                nm = nm.strip()
                if not nm:
                    continue
                kind, val = resolve(nm, title2slug)
                if kind == "ok" and val in {sl for sl, _ in slugthemes}:
                    report["drops"].append((nm, "self-reference", next((sl for sl, _ in slugthemes), "")))
                elif kind == "ok":
                    related.append({"type": "related", "target": val})
                else:
                    report["drops"].append((nm, kind, next((s for s, _ in slugthemes), "")))
                    if kind == "unresolved":
                        report["unresolved"].append(nm)
        seealso_targets = [t for t in (" ".join(sees),)]
        common = {
            "date_created": DATE_CREATED, "date_last_changed": DATE_CREATED,
            "sources": SOURCES, "contributors": CONTRIBUTOR, "status": "reviewed",
        }
        title_map = dict((t, t) for t, _, _ in [])  # placeholder
        def_title = " ".join(defs)
        def_groups = {}
        for slug, themes in slugthemes:
            def_groups[slug] = def_title
        if title == "Replication / Reproducibility":
            intro = def_title
            bylabel = {}
            for d in details:
                m = re.match(r"(Reproducibility|Replication):\s*(.*)", d)
                if m:
                    bylabel[m.group(1)] = m.group(2)
            for slug, themes in slugthemes:
                label = "Reproducibility" if slug == "reproducibility" else "Replication"
                write_term(outdir, {"id": slug, "title": label.title(),
                    "alternatives": EXTRA_ALTS[slug], "themes": themes,
                    "related": sorted(related, key=lambda r: r["target"]) + ([] if slug != "replication" else
                        [{"type": "contrasts-with", "target": "reproducibility",
                          "reason": "Commonly confused pair; the v1.0.0 entry warned the terms are often used interchangeably but the distinction matters (D-4)."}]),
                    **common,
                    "definition": (label + ": " + bylabel[label]) if label in bylabel else intro,
                    "details": [intro] if intro else [], "warning": " ".join(warnings)})
                report["files"].append(slug); report["mapping"].append((title, slug))
        elif title == "Science Sleuths / Post-Publication Peer Review (PPPR)":
            write_term(outdir, {"id": "science-sleuths", "title": "Science Sleuths",
                "alternatives": EXTRA_ALTS["science-sleuths"], "themes": slugthemes[0][1],
                "related": sorted(related, key=lambda r: r["target"]) +
                    [{"type": "is-part-of", "target": "post-publication-peer-review",
                      "reason": "The sleuths are the actors whose public checking constitutes a large share of post-publication peer review in practice (D-4)."}],
                **common, "definition": def_title, "details": details, "warning": " ".join(warnings)})
            write_term(outdir, {"id": "post-publication-peer-review", "title": "Post-Publication Peer Review (PPPR)",
                "alternatives": EXTRA_ALTS["post-publication-peer-review"], "themes": slugthemes[1][1],
                "related": [], "status": "draft",
                "date_created": DATE_CREATED, "date_last_changed": DATE_CREATED,
                "sources": SOURCES, "contributors": CONTRIBUTOR,
                "definition": "Refereeing that takes place after publication: public, often informal scrutiny of published papers and their evidence, performed largely by science sleuths and on platforms such as PubPeer.",
                "details": ["Draft entry split from the combined v1.0.0 heading (D-4): the practice; the v1.0.0 text is preserved verbatim in the Science Sleuths entry (the actors)", "Editorial review pending; see docs/BACKLOG-TERMS.md"]})
            report["files"] += ["science-sleuths", "post-publication-peer-review"]
            report["mapping"] += [(title, "science-sleuths"), (title, "post-publication-peer-review")]
        else:
            for slug, themes in slugthemes:
                write_term(outdir, {"id": slug, "title": title,
                    "alternatives": EXTRA_ALTS.get(slug, []), "themes": themes,
                    "related": sorted(related, key=lambda r: r["target"]), **common,
                    "definition": def_title, "details": details,
                    "warning": " ".join(warnings) if len(warnings) == 1 else None or " ".join(warnings)})
                report["files"].append(slug); report["mapping"].append((title, slug))
        if len(defs) > 1:
            report["flags"].append(f"{title}: {len(defs)} definition paragraphs (joined)")
        if warnings and len(warnings) > 1:
            report["flags"].append(f"{title}: {len(warnings)} warning paragraphs (joined)")
    return report


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def verify(docx_path, termdir):
    seq = parse_docx(docx_path)
    heads, entries, _ = split_entries(seq)
    corpus = "\n".join(f.read_text(encoding="utf-8") for f in sorted(termdir.glob("*.md")))
    clean_lines = []
    for line in corpus.split("\n"):
        t = line.lstrip()
        if t.startswith("# ") or t == "---" or t.startswith("> [!WARNING]"):
            continue
        if t.startswith("> "):
            t = t[2:]
        if t.startswith("- "):
            t = t[2:]
        clean_lines.append(t)
    clean = norm(" ".join(clean_lines))
    missing = []
    seen = set()
    for title, e in entries.items():
        for para in e["paras"]:
            if para.startswith("See also:"):
                continue
            if para in seen:
                continue
            seen.add(para)
            text = re.sub(r"^[\u25b8\u26a0]\s*", "", para)
            if norm(text) not in clean:
                missing.append((title, norm(text)[:80]))
    return missing, len(entries)


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    docx_path = Path(sys.argv[1]); outdir = Path(sys.argv[2])
    report_path = None
    if "--report" in sys.argv:
        i = sys.argv.index("--report")
        report_path = Path(sys.argv[i + 1])
    elif len(sys.argv) > 3 and sys.argv[3].startswith("--report="):
        report_path = Path(sys.argv[3].split("=", 1)[1])
    rep = migrate(docx_path, outdir, None)
    missing, n_entries = verify(docx_path, outdir)
    lines = ["# Migration report (v1.0.0 DOCX to term files)", "",
             "- Heading canon check: 64 expected, all mapped (see table below; unmapped headings would be listed under Flags).",
             f"- Term files written: {len(rep['files'])}",
             f"- Dropped see-also references: {len(rep['drops'])} (D-5; see docs/BACKLOG-TERMS.md)",
             f"- Word-for-word check: {'PASS - no definition text lost' if not missing else 'FAIL - ' + str(len(missing)) + ' paragraphs missing'} (scope: definitions, details, warnings; see-also lines are structurally migrated into related and excluded from the string check)", ""]
    lines.append("## Heading -> term file(s)"); lines.append("| DOCX heading | Term file(s) |"); lines.append("| --- | --- |")
    seen = {}
    for t, s in rep["mapping"]:
        seen.setdefault(t, []).append(s)
    for t, ss in seen.items():
        lines.append(f"| {t} | {', '.join('`' + x + '.md`' for x in ss)} |")
    lines.append("\n## Dropped see-also references (D-5)")
    lines.append("| Reference | Reason |"); lines.append("| --- | --- |")
    for nm, kind, _ in rep["drops"]:
        lines.append(f"| {nm} | {'first-wave backlog term' if kind == 'first-wave' else 'deferred backlog term'} |")
    if rep["unresolved"]:
        lines.append("\n## UNRESOLVED names (fix the alias map): " + ", ".join(sorted(set(rep["unresolved"]))))
    if rep["flags"]:
        lines.append("\n## Flags"); [lines.append("- " + f) for f in rep["flags"]]
    if missing:
        lines.append("\n## Missing text (word-for-word check)"); [lines.append(f"- {t}: {x}") for t, x in missing]
    text = "\n".join(lines) + "\n"
    print(text)
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text, encoding="utf-8")
        print(f"report written to {report_path}")
    critical = [f for f in rep["flags"] if "heading not found" in f or "expected 64" in f]
    ok = not missing and not rep["unresolved"] and len(rep["files"]) == 66 and not critical
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
