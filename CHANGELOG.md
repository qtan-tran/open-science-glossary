# Changelog

All notable changes to the Open Science Glossary website are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/): a content release that changes
the edition counts as a major version (the Word/PDF edition was v1.0.0).

## 2.0.0 (unreleased)

First edition of the website (successor of the Word/PDF edition v1.0.0,
archived on Zenodo as
[10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750)).
Per maintainer decision of 2026-11-20, the website edition itself is not
published on Zenodo and carries no version DOI; the live website is the
edition, cited by its URL.

### Added

- Website (Hugo, version pinned per D-2): A-Z index, per-term pages at
  /term/<slug>/ with bidirectional typed relationships (PR #9), theme pages,
  Quick-Reference sheet generated from the term files (D-11), per-term APA +
  BibTeX citations (D-6), and a BibTeX export for all terms.
- Machine-readable core: YAML term files with JSON Schema validation,
  closed vocabularies for themes and relationship types, stdlib-only
  migration and validation scripts, CI gates on every push and pull request.
- Second-wave new terms, maintainer-approved and reviewed 2026-11-20: cOAlition S, Copyright Transfer, Rights Retention
  Strategy, Open Infrastructure, Black Box (Latour), Community Archive,
  Wikisource, OSF, arXiv, SocArXiv, Think. Check. Submit., Data Steward,
  Open Notebook Science, Peer Community In (PCI), Unpaywall, OA Button
  (16 new entries total).
- Third-wave new terms, maintainer-approved and reviewed 2026-11-20: bioRxiv, medRxiv, openRxiv, LOCKSS,
  CLOCKSS, NISO, JATS, Jisc, Review Commons, COPIM, Opening the Future,
  Open Journals Collective, OpenAPC, openCost, Finch Report, Stockholm
  Declaration (2025), OA2020, OASPA, COPE, WCRI, Nelson Memo, UKRI, One
  Nation One Subscription, SPARC, ARL, ALPSP, Research4Life, FWCI, JCR,
  Times Higher Education rankings, Information Power guidance, BioMed
  Central, Annual Reviews, Subscribe to Open, SAGE Open, F1000Research,
  UK Biobank, Library Consortium, Consortium Couperin, SANLiC, Hoax
  paper (41 new entries total, bringing the corpus to 135).
- Fourth-wave new terms, drafted 2026-11-20 (status `draft`, maintainer
  review pending): Wikipedia, Wiki Goes MEK, Open Cultural Heritage,
  Digital Heritage, OA monograph (5 new entries, bringing the corpus to
  140).
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
- Zenodo description correction (D-11) cancelled with the Zenodo release
  itself (maintainer decision 2026-11-20): the v1.0.0 record and its "55
  terms" wording stay as published in 2026-10; the website edition carries
  the corrected counts.

### Fixed

- Third-wave fact-check sweep (maintainer-requested, 2026-11-20):
  corrected the Couperin full name (Consortium unifié des établissements
  universitaires et de recherche pour l'accès aux publications
  numériques, founded 1999, 250-plus member institutions), the openCost
  project partners (Bielefeld University Library, DESY Hamburg,
  Regensburg University Library), the OpenAPC maintenance attribution
  (Bielefeld University Library since 2014), and expanded the Open
  Journals Collective entry with verified launch-collection and
  investment-campaign details.

## 1.0.0 (2026-10-18)

Word/PDF edition published on Zenodo
([10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750),
CC BY 4.0): 64 full entries, 54-row Quick-Reference sheet.
