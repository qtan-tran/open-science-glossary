# Rebuild notes (D-2, ADR-0008)

The site is a build product; the term files in `content/terms/` and the
vocabularies in `data/` are the single source of truth. This document records
everything needed to rebuild the site if the current static site generator is
ever abandoned. Per D-2: the exact Hugo version is pinned in CI and in the
README, all templates live in this repository, and no external themes are used.

## Contract any rebuild must satisfy

1. Input: `content/terms/*.md` (YAML front matter validated by
   `schemas/term.schema.json` and `scripts/validate.py`), `data/*.yaml`.
2. Output: plain static files (HTML, CSS, and the SKOS/JSON-LD/CSV exports of
   ADR-0005), deployable on any static host with no server-side code.
3. Core reading experience works without JavaScript (ADR-0006); any optional
   layer (e.g. a relationship graph) degrades to an accessible table that is
   present in the static output.
4. Every term gets a stable URL of the form `/terms/<slug>/`; nothing is ever
   renamed, only deprecated and replaced (DATA-MODEL.md).
5. The word-for-word migration gate (`scripts/check_migration.py`) and the
   validator keep passing.

## Hugo specifics (filled in during Phase 1)

- Hugo version: to be pinned here and in CI when the skeleton lands
  (D-2 requires the exact version).
- Layouts: `layouts/` in this repository; no theme modules.
- Build: `hugo --gc --minify` (exact invocation recorded here in Phase 1).
- Deprecation path: if Hugo is abandoned, a new generator reads the same term
  files and vocabularies; no content migration should ever be needed.
