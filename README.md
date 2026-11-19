# Open Science Glossary

A bilingual (English first, German pilot planned), machine-readable glossary of
open science terms, evolved from the Word/PDF edition v1.0.0
([Zenodo concept DOI 10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750), CC BY 4.0).

The canon is the 64 full entries of the v1.0.0 Word edition. After the D-4
splits (Replication / Reproducibility; Science Sleuths / Post-Publication Peer
Review) that is 66 term files in v2.0.0, plus first-wave new terms
(docs/DECISIONS.md, D-5) as they are finished. The old combined labels are kept
as `alternatives` so existing links keep resolving.

## Status

- Planning: complete (docs/, ADRs 0001-0009, decisions D-1 to D-12; PR #1).
- Phase 0: tooling done. One data file per term in `content/terms/`, controlled
  vocabularies, JSON Schema, stdlib-only migration and validation scripts (no
  third-party dependencies; see requirements.txt).
- Phase 1 (next): Hugo site skeleton, pinned exact version (recorded here and
  in CI), templates kept in-repo, no external themes.

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
legacy/                   v1.0.0 DOCX + PDF export; the record of the original
                          publication; never edited after commit (D-1)
docs/                     planning: concept, data model, architecture, roadmap,
                          decisions D-1 to D-12, open-questions (resolved),
                          backlog terms, ADRs, rebuild notes
```

## Working on the repo

Python 3.9+ standard library only, no installs required:

```bash
python3 scripts/validate.py content/terms
python3 scripts/check_migration.py legacy/OpenScience_Glossary.docx content/terms
python3 scripts/migrate_v1.py legacy/OpenScience_Glossary.docx content/terms --report docs/migration-report.md
```

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
