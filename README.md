# Open Science Glossary

A bilingual (English first, German pilot planned), machine-readable glossary of
open science terms, evolved from the Word/PDF edition v1.0.0
([Zenodo concept DOI 10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750), CC BY 4.0).

## Read the glossary

**Website: <https://qtan-tran.github.io/open-science-glossary/>**
(live as soon as the Pages source is set to "GitHub Actions";
see [issue #8](https://github.com/qtan-tran/open-science-glossary/issues/8)).

Nothing to install and nothing to run: the site is plain HTML and CSS,
generated ahead of time and served by GitHub Pages. Any browser opens the
A-Z index, every term page (/term/<slug>/), the theme pages and the
quick-reference sheet. A BibTeX export of all terms is downloadable at
/downloads/open-science-glossary.bib, and the original v1.0.0 edition
(DOCX + PDF) stays in the
[Zenodo record](https://doi.org/10.5281/zenodo.23449750).
The Python and Hugo commands further below are maintainer tooling only;
readers never need them.

The canon is the 64 full entries of the v1.0.0 Word edition. After the D-4
splits (Replication / Reproducibility; Science Sleuths / Post-Publication Peer
Review) that is 66 term files in v2.0.0, plus first-wave new terms
(docs/DECISIONS.md, D-5): the eleven first-wave entries (with Retraction
Watch and PubPeer split into two entries) were drafted on 2026-11-20, in
`draft` status until reviewed. The old combined labels are kept
as `alternatives` so existing links keep resolving.

## Status

- Planning: complete (docs/, ADRs 0001-0009, decisions D-1 to D-12; PR #1).
- Phase 0: complete (PR #2). 66 term files migrated from the v1.0.0 DOCX,
  machine-verified word-for-word; stdlib-only migration and validation tooling.
- Phase 1: site skeleton complete (PR #3). Hugo v0.170.0 (exact version
  pinned in CI and in the checksummed download; D-2), templates in-repo, no
  external themes, no JavaScript for the reading core (ADR-0006). Term pages
  at /term/<slug>/, themes at /theme/<id>/, A-Z index, /quick-reference/
  generated from the term files (D-11), per-term APA + BibTeX citations
  (concept DOI until the first version DOI mints, D-6), BibTeX export of all
  terms, GitHub Pages deploy workflow, and the w3id .htaccess ready for the
  upstream registration (ADR-0003).
- Phase 2 first wave: the eleven D-5 terms drafted (12 files, Retraction Watch
  and PubPeer split per D-4 practice), maintainer-reviewed 2026-11-20
  (status `reviewed`).
- Phase 2 second wave: sixteen additional entries maintainer-approved,
  drafted and reviewed on 2026-11-20 (see docs/BACKLOG-TERMS.md).

## Repository map

```text
content/terms/            one Markdown + YAML front-matter file per term (single source of truth)
data/themes.yaml          closed theme vocabulary
data/relationship-types.yaml  closed typed-relation vocabulary
data/languages.yaml       language metadata (EN reviewed, DE pilot)
schemas/term.schema.json        JSON Schema (draft-07) for a term file
schemas/vocabulary.schema.json  JSON Schema for a vocabulary YAML file
scripts/migrate_v1.py     one-shot migration from the legacy DOCX into term files
scripts/check_migration.py Phase 0 acceptance gate (headings map, word-for-word check; D-11)
scripts/validate.py       lint term files (slug/theme/relation rules, D-5 fail-hard)
scripts/export_bib.py     BibTeX export of all terms (same entries the site renders)
layouts/, assets/, hugo.toml  the site; one small CSS file, zero JS (ADR-0006)
.github/workflows/        validate.yml (data + build gates), deploy.yml (Pages)
ids/os-glossary/          mirror of the w3id.org redirect registration (ADR-0003)
legacy/                   v1.0.0 DOCX + PDF export; the record of the original
                          publication; never edited after commit (D-1)
docs/                     planning: concept, data model, architecture, roadmap,
                          decisions D-1 to D-12, open-questions (resolved),
                          backlog terms, ADRs, rebuild notes
```

## Maintainer toolkit (readers can skip this)

Everything in this section is only needed to edit and re-verify the glossary.
CI runs the same checks on every push and pull request, so contributors do
not need Python or Hugo installed on their own machines either.

Python 3.9+ standard library only, no installs required:

```bash
python3 scripts/validate.py content/terms
python3 scripts/export_bib.py content/terms static/downloads/open-science-glossary.bib
python3 scripts/check_migration.py legacy/OpenScience_Glossary.docx content/terms
python3 scripts/migrate_v1.py legacy/OpenScience_Glossary.docx content/terms --report docs/migration-report.md
```

Build the site with the pinned generator (v0.170.0; D-2):

```bash
hugo --minify --printPathWarnings   # static output in public/, no JS, no themes
```

Everything above is standard-library Python plus the single pinned Hugo binary;
no package installs (requirements.txt stays empty).

CI (`.github/workflows/validate.yml`) runs the validator and the schema/vocabulary
checks on every push and pull request. Any `related` entry pointing at a term
that has no term file fails the build (D-5).

## Identity, versioning, licensing

- Permanent term URLs will live under `https://w3id.org/os-glossary/...`
  (namespace confirmed unclaimed at registration time; no institution names, D-12).
- Semantic versioning; the site era starts at v2.0.0 because the format and data
  model change (D-3). New versions are published as new versions of the existing
  Zenodo record, so the whole Word-to-site history keeps one concept DOI.
- Content: CC BY 4.0 (`LICENSE-CONTENT`). Code: MIT (`LICENSE-CODE`). See
  ADR-0007.

## Credits

Created and maintained by Quoc-Tan Tran (ORCID 0000-0003-3533-5858).
Institutional context in the About page and history (D-12); this project is
independently maintained.
