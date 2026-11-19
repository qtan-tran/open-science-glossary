#!/usr/bin/env python3
"""export_bib.py -- generate a BibTeX file from the term files (ROADMAP 1.3).

The same entries the term pages render in their "Cite this term" box, kept
consistent by construction: both are deterministic functions of the front
matter. Standard library only.

Usage: python3 scripts/export_bib.py <terms-dir> <output.bib>
Exit 0 on success; fails if any entry does not parse or braces do not balance.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # reuses the stdlib front-matter parser  # noqa: E402

VERSION = "2.0.0"
CONCEPT_DOI = "10.5281/zenodo.23449750"
PERMANENT_BASE = "https://w3id.org/os-glossary"


def bibtex_escape(s):
    return s.replace("{", "\\{").replace("}", "\\}")


def entry(fm):
    authors = []
    for c in fm.get("contributors") or []:
        if isinstance(c, dict) and c.get("name"):
            authors.append(str(c["name"]))
    author = " and ".join(authors) or "Tran, Quoc-Tan"
    year = str(fm.get("date_last_changed", "2026"))[:4]
    title = str(fm.get("title", ""))
    tid = str(fm.get("id", ""))
    # double braces protect capitalisation in titles
    t = "{{" + title.replace("{", "").replace("}", "") + "}}"
    url = f"{PERMANENT_BASE}/term/{tid}"
    return (
        f"@misc{{osg_{tid},\n"
        f"  author = {{{author}}},\n"
        f"  title = {t},\n"
        f"  year = {{{year}}},\n"
        f"  howpublished = {{Open Science Glossary}},\n"
        f"  note = {{Version {VERSION}. {url}}},\n"
        f"  doi = {{{CONCEPT_DOI}}}\n"
        f"}}"
    )


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    termdir, out = Path(sys.argv[1]), Path(sys.argv[2])
    files = sorted(termdir.glob("*.md"))
    chunks = [
        "% BibTeX for the Open Science Glossary, generated from the term files.",
        f"% Version {VERSION}; concept DOI {CONCEPT_DOI}. Do not edit by hand.",
        "",
    ]
    for f in files:
        fm = validate.parse_front_matter(f.read_text(encoding="utf-8"))
        chunks.append(entry(fm))
        chunks.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(chunks), encoding="utf-8")
    text = out.read_text(encoding="utf-8")
    assert text.count("{") == text.count("}"), "unbalanced braces in generated .bib"
    n = text.count("@misc{osg_")
    print(f"wrote {out}: {n} entries from {len(files)} term files")
    return 0 if n == len(files) else 1


if __name__ == "__main__":
    sys.exit(main())
