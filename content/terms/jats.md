---
id: "jats"
title: "JATS"
alternatives:
- "Journal Article Tag Suite"
themes:
- "infrastructure"
- "publishing"
status: "reviewed"
date_created: "2026-11-20"
date_last_changed: "2026-11-20"
sources:
- text: "ANSI/NISO Z39.96, The JATS (Journal Article Tag Suite) standard, NISO"
  url: "https://jats.niso.org/"
contributors:
- name: "Quoc-Tan Tran"
  orcid: "0000-0003-3533-5858"
  role: "author"
related:
- type: "related"
  target: "niso"
- type: "related"
  target: "crossref"
- type: "related"
  target: "preprint"
---

JATS (Journal Article Tag Suite) is an XML standard (ANSI/NISO Z39.96) for encoding the full text and metadata of scholarly journal articles, enabling consistent publication, archiving, and exchange of articles across platforms.

## Details

- **What it encodes:** Front matter (authors, affiliations, DOIs, licence information), body text with figures and tables structured by section, and back matter including reference lists, all in one tagged document.
- **Adoption:** JATS is the deposit format of PubMed Central and the basis of publishing pipelines and full-text hosting for many presses, platforms, and repositories.
- **Extensibility:** The standard is provided in three "tag sets" with different strictness (strict, simplified, indexing) so it can serve close-to-production publishing as well as large-scale indexing.
- **Open science value:** Because the full text, not just the abstract, is machine-readable, JATS is a foundation for text mining, reproducible archiving, and open citation analysis.

> [!NOTE]
> Preprint servers such as bioRxiv and medRxiv accept JATS-structured deposits where available, which makes preprint-to-journal transfers possible without re-typesetting.
