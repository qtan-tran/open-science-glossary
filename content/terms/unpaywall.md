---
id: "unpaywall"
title: "Unpaywall"
themes:
- "infrastructure"
- "publishing"
status: "reviewed"
date_created: "2026-11-20"
date_last_changed: "2026-11-20"
sources:
- text: "OpenAlex, Unpaywall product documentation (launched 2017; moved onto the OpenAlex database in late 2025)"
  url: "https://unpaywall.org/"
contributors:
- name: "Quoc-Tan Tran"
  orcid: "0000-0003-3533-5858"
  role: "author"
related:
- type: "enables"
  target: "green-oa"
  reason: "Unpaywall surfaces legally self-archived manuscript copies across the whole literature, making the scattered green OA layer usable at scale."
- type: "related"
  target: "open-access"
- type: "related"
  target: "repository"
- type: "related"
  target: "oa-button"
- type: "related"
  target: "doi"
---

A free service, launched in 2017 by the nonprofit OurResearch and run since late 2025 on the OpenAlex database, that answers one question for every article with a DOI: is there a legal free-to-read copy, and where? It appears as a small browser extension (a green or grey lock on the publisher page) and, more importantly, as a public API and dataset that libraries, search engines and assessment tools query by the millions.

## Details

- For each article it classifies the best open location found (gold publisher copy, green repository copy, hybrid) and exposes the licence when known
- Because the underlying data is public, it has become the de facto measurement instrument for open access shares of the literature, used in funders' monitoring (in adaptation) and in research on the OA landscape
- The same team also built OpenAlex, the open scholarly graph, and the two systems now share one database

> [!WARNING]
> A green lock means a legal copy was found somewhere, not that the copy is the version of record, complete, or permanently kept alive: link rot in repositories degrades the green layer over time