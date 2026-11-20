---
id: "lockss"
title: "LOCKSS"
alternatives:
- "Lots of Copies Keep Stuff Safe"
themes:
- "infrastructure"
status: "reviewed"
date_created: "2026-11-20"
date_last_changed: "2026-11-20"
sources:
- text: "LOCKSS Program, Stanford University Libraries"
  url: "https://www.lockss.org/"
contributors:
- name: "Quoc-Tan Tran"
  orcid: "0000-0003-3533-5858"
  role: "author"
related:
- type: "related"
  target: "clockss"
- type: "related"
  target: "repository"
- type: "related"
  target: "version-of-record"
---

LOCKSS ("Lots of Copies Keep Stuff Safe") is an open-source digital preservation program developed at Stanford University. It enables libraries to preserve web-published scholarly content by having each participating institution run a local server that continuously collects and verifies copies of e-journals, e-books, and other material.

## Details

- **How it works:** A library's LOCKSS server polls publishers' sites for new content and exchanges checksums with peer servers, so damage or loss at one site is repaired from the other copies.
- **Principle:** Preservation through redundant copying across many independent institutions, rather than a single central archive.
- **Origin:** Developed from 2000 onward as a direct response to the licensing problem of e-journals: if a library only licenses access, the content disappears when the subscription or the publisher does.
- **Ecosystem:** LOCKSS technology underpins several preservation services, including CLOCKSS and private preservation networks run by library consortia.

> [!NOTE]
> LOCKSS-preserved content is normally served to readers only when the library's subscription or the publisher's platform fails, so day-to-day reading still happens at the publisher's site.
