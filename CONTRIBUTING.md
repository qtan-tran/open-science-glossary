# Contributing to the Open Science Glossary

Corrections, improvements and new terms are welcome from anyone. This is a
community-friendly project with a single maintainer making final calls.

## Governance (for now)

- The maintainer (Quoc-Tan Tran) decides what is merged.
- All changes come in by pull request, including the maintainer's own changes.
- Corrections from anyone are welcome; substantive new terms or scope changes
  should be proposed as an issue first.
- A short entry in the changelog and a `date_last_changed` bump are part of
  every content change.

The full `GOVERNANCE.md`, including how a successor takes over the project,
arrives in Phase 6 of docs/ROADMAP.md (decision D-10).

## How to edit content

- One Markdown file per term in `content/terms/`, slug as filename, YAML front
  matter per docs/DATA-MODEL.md and `schemas/term.schema.json`.
- Closed vocabularies only: `themes` must come from `data/themes.yaml`, relation
  `type` from `data/relationship-types.yaml`.
- A `related` entry whose `target` has no term file fails the build (D-5). If a
  term you want to reference does not exist yet, either add it as an alias of
  an existing term or park it in docs/BACKLOG-TERMS.md and drop the reference.
- `reason` is required on every typed relation except plain `related`.
- Splits and renames keep the old label in `alternatives` so existing links and
  searches keep working (see the D-4 entries for the pattern).

## Before you open a PR

```bash
python3 scripts/validate.py content/terms
python3 scripts/check_migration.py legacy/OpenScience_Glossary.docx content/terms
```

Both must pass. CI runs the same checks. No third-party Python packages are
needed or accepted in the pipeline.

## Licences

By submitting content you agree it is licensed CC BY 4.0; code is MIT
(ADR-0007). The project does not copy text from NC/ND-licensed sources such as
the FORRT glossary (linked via `skos:closeMatch`, never copied).
