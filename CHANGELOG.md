# Changelog

All notable changes to the Open Science Glossary website are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/): a content release that changes
the edition counts as a major version (the Word/PDF edition was v1.0.0).

## 2.0.0 (unreleased)

First edition of the website (successor of the Word/PDF edition v1.0.0,
Zenodo concept DOI [10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750)).

### Added

- Website (Hugo, version pinned per D-2): A-Z index, per-term pages at
  /term/<slug>/ with bidirectional typed relationships (PR #9), theme pages,
  Quick-Reference sheet generated from the term files (D-11), per-term APA +
  BibTeX citations (D-6), and a BibTeX export for all terms.
- Machine-readable core: YAML term files with JSON Schema validation,
  closed vocabularies for themes and relationship types, stdlib-only
  migration and validation scripts, CI gates on every push and pull request.
- Second-wave new terms, maintainer-approved 2026-11-20 (`draft` status
  until reviewed): cOAlition S, Copyright Transfer, Rights Retention
  Strategy, Open Infrastructure, Black Box (Latour), Community Archive,
  Wikisource, OSF, arXiv, SocArXiv, Think. Check. Submit., Data Steward,
  Open Notebook Science, Peer Community In (PCI), Unpaywall, OA Button
  (16 new entries total).
- Typed relationships between terms (PR #9): is-part-of, responds-to,
  enables, contributes-to, constrains, contrasts-with.
- First-wave new terms (D-5), maintainer-reviewed on 2026-11-20 (status
  `reviewed`): Open Science,
  Open Data, Open Educational Resources, DOAJ, Publication Bias, Indigenous
  Data Sovereignty, Serials Crisis / Big Deal, Bibliometrics, Altmetrics,
  PKP, Retraction Watch, PubPeer (12 files; Retraction Watch and PubPeer
  split into two entries following the D-4 practice).

### Changed

- The canon becomes the 64 v1.0.0 entries plus the D-4 splits: 66 migrated
  term files are the single source of truth; the legacy DOCX and PDF stay in
  legacy/ untouched (D-1).
- Combined v1.0.0 entries split for precision (D-4): Replication /
  Reproducibility; Science Sleuths / Post-Publication Peer Review. The old
  combined labels remain as `alternatives`.
- Zenodo record description will be corrected at release: v1.0.0 said
  "55 terms" (the Quick-Reference sheet); the edition actually has 64 full
  entries (D-11).

## 1.0.0 (2026-10-18)

Word/PDF edition published on Zenodo
([10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750),
CC BY 4.0): 64 full entries, 54-row Quick-Reference sheet.
