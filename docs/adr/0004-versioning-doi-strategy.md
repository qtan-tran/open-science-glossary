# ADR-0004: Versioning and DOI strategy

Status: accepted, revised 2026-11-19 (maintainer decision D-3; revises the original "new record" proposal during planning review)

## Context

The glossary must stay citable as a whole and per release. Zenodo's GitHub integration mints each release of a connected repository as a new version of that integration's own record (one concept DOI per repository); per Zenodo's documentation a repository cannot be attached to an existing concept DOI. v1.0.0 (Word/PDF) is Zenodo record 10.5281/zenodo.23449750. The maintainer's decision (D-3): the glossary keeps **one concept DOI from the Word edition onward**.

## Options considered

1. **New Zenodo record via the GitHub integration** (original proposal). Fully automatic per release, but it would break the citation line: a second concept DOI at the platform change, and a record split the maintainer explicitly rejects.
2. **Keep the existing record: publish v2.0.0+ as new versions of record 10.5281/zenodo.23449750.** New versions are created in the Zenodo web UI ("new version") or via the Zenodo REST API, uploading the release assets per release. The GitHub integration is then not used for publishing at all. **Chosen (D-3).**

## Decision

1. **Semver policy:** the first site release is tagged **v2.0.0**. The major bump flags the change of format and data model (Word document -> structured data + website). Minor versions add terms or languages; patches fix content errors. v1.x remains the Word/PDF era.
2. **One DOI chain:** every release v2.0.0+ is published as a **new version of Zenodo record 10.5281/zenodo.23449750**. The concept DOI therefore covers the whole glossary line from v1.0.0 onward. Record metadata (description wording, e.g. term counts, D-11) is maintained per release.
3. **Publishing route:** manual upload via the Zenodo web UI or the Zenodo REST API, following the release checklist. Smoke-test the version-workflow on sandbox.zenodo.org before the first real release (per Zenodo guidance). The GitHub integration is NOT connected for publishing, because it cannot attach to the existing record (verified against Zenodo's documentation; see ARCHITECTURE section 4).
4. **Release assets** per version: built site ZIP, CSV/JSON/SKOS exports, printable Quick-Reference sheet, source snapshot. The rendered site is thereby frozen per version DOI.
5. **Citation payload:** the whole glossary cites the concept DOI; term pages cite the permanent URL (w3id, ADR-0003) plus the current release's version DOI. **No per-term DOIs** (D-6): term identity is the permanent URL; per-term DOIs would multiply maintenance cost for near-zero citation benefit.
6. **CITATION.cff** in the repo root carries the concept DOI and per-release version metadata (filled at release time); the Zenodo record title/description stays accurate ("terms" counts corrected at v2.0.0, D-11).
7. **Software Heritage** archives the git repository per release (ADR-0008); Zenodo keeps the frozen version artefacts. If Zenodo ever forced a record split, cross-link via related identifiers both ways and document it in the README and CHANGELOG.

## Consequences

- Citation continuity: a reader citing "the Open Science Glossary" uses one stable concept DOI whether they cite v1.0.0 (PDF) or v5.3.0 (site).
- One manual step per release (create the new version, upload assets, fill metadata; ~10 minutes) replaces the automatic integration. This is the accepted price of the single DOI chain.
- Tagging discipline remains: semver tags + generated CHANGELOG are the machine-readable chronicle that Zenodo metadata mirrors.
- Sandbox rehearsal (sandbox.zenodo.org) before v2.0.0 avoids mis-published versions on the live record, which cannot be deleted once public.

## Note on the superseded proposal

The original proposal (new record + cross-linked related identifiers in both directions) is preserved in the PR history of this ADR for the record. It remains the documented fallback if the existing record ever becomes unavailable or unmaintainable.
