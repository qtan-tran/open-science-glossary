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

## Hugo specifics (filled in during Phase 1, 2026-11-19)

- Hugo version: **v0.170.0**, exact version pinned in `.github/workflows/*.yml`
  (`HUGO_VERSION` + `HUGO_SHA256` checksum `0930754ec22ad2dd1a252f8c31a5e57faccc9d15f1c3d381ddafcb96eeb8aef0`).
  Bumping = change those two values, rebuild, fix anything that changed.
  Note: since v0.170.0 there is no separate "extended" edition.
- Layouts: `layouts/` in this repository; no theme modules, no external
  assets, one CSS file, no JavaScript.
- Build: `hugo --minify --printPathWarnings` produces `public/`; CI must build
  with zero warnings (ROADMAP 1.1 acceptance).
- URLs: term pages at `/term/<slug>/` (permalink token `:slugorfilename`, which
  equals the term id because files are named by id), theme pages at
  `/theme/<id>/`; both mirror the w3id path shape (ADR-0003).
- Front matter: Hugo reads the migration YAML directly; `scripts/validate.py`
  remains the source of truth for its rules, and `scripts/export_bib.py`
  regenerates the same citation entries the templates render.
- GitHub Pages: deploy via `.github/workflows/deploy.yml` (Actions source must
  be selected once in repo Settings > Pages). The output is plain files;
  `docs/rebuild.md` plus `content/terms/` + `data/` are enough to rebuild
  the identical site on any other static host or generator.
- Deprecation path: if Hugo is abandoned, a new generator reads the same term
  files and vocabularies; no content migration should ever be needed.
