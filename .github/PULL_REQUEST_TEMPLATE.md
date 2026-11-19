## What changes?

<!-- One or two sentences. -->

## Which decision applies?

<!-- docs/DECISIONS.md D-number(s), e.g. D-4 for term splits, D-5 for new terms/aliases. -->

## Checks

- [ ] `python3 scripts/validate.py content/terms` passes locally
- [ ] `python3 scripts/check_migration.py legacy/OpenScience_Glossary.docx content/terms` passes (if content changed)
- [ ] No see-also/related targets are missing term files (build fails otherwise, D-5)
