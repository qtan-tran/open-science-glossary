---
id: "fwci"
title: "FWCI"
alternatives:
- "Field-Weighted Citation Impact"
themes:
- "assessment"
status: "reviewed"
date_created: "2026-11-20"
date_last_changed: "2026-11-20"
sources:
- text: "Elsevier, SciVal metrics definitions: Field-Weighted Citation Impact"
  url: "https://www.scival.com/"
contributors:
- name: "Quoc-Tan Tran"
  orcid: "0000-0003-3533-5858"
  role: "author"
related:
- type: "contrasts-with"
  target: "impact-factor"
  reason: "FWCI normalizes citations at the article level by field, year, and document type, correcting precisely what the journal-level Journal Impact Factor is criticized for."
- type: "related"
  target: "bibliometrics"
- type: "related"
  target: "h-index"
- type: "related"
  target: "jcr"
---

Field-Weighted Citation Impact (FWCI) is a bibliometric indicator developed by Elsevier (from Scopus data) that measures how often a publication is cited compared with the world average for similar publications, controlling for field, publication year, and document type.

## Details

- **Interpretation:** An FWCI of 1.00 means the paper is cited exactly at the world average for its field, year, and type; 2.00 means twice that average.
- **Granularity:** Unlike the Journal Impact Factor, FWCI is computed at the level of single publications (and averages over portfolios), so it can be attached to an individual output.
- **Advantages:** Normalization by field and year addresses the two biggest biases of raw citation counts; document-type control keeps reviews from drowning out research articles.

> [!WARNING]
> FWCI still measures attention within the citation system, not quality or reproducibility, and it inherits Scopus's coverage choices; using it as the sole indicator in research assessment reproduces the same metric-driven problems as any other single number.
