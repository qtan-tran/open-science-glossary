# CONCEPT — Open Science Glossary website

Status: approved 2026-11-19 (maintainer review; decisions in [DECISIONS.md](DECISIONS.md))
Owner: Quoc-Tan Tran (ORCID [0000-0003-3533-5858](https://orcid.org/0000-0003-3533-5858))
Companion docs: [DATA-MODEL.md](DATA-MODEL.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ROADMAP.md](ROADMAP.md) · [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) · [DECISIONS.md](DECISIONS.md)

## 1. Background and purpose

The Open Science Glossary accompanies the bachelor's seminar **Introduction to Open Science** (Universität Hamburg, Winter Semester 2026/27). Version 1.0.0 exists as a PDF document archived on Zenodo ([DOI 10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750)): terms A–Z, each with a definition, bullet-point details, a common-misconception warning, and see-also references.

This project turns that document into a **public website** that can grow over the years and remains citable. Two things change fundamentally:

1. **Structure over alphabet.** The document's only navigation is the alphabet. The site adds *themes* (controlled vocabulary, e.g. Publishing models & economics, Global equity & epistemic justice, Research integrity) so that a reader can approach the material the way the seminar teaches it: not "what does APC mean?" but "how does the money flow in open access, and who is excluded by it?"
2. **Typed relations over loose cross-references.** The document's "see also" pointers become directional, labelled statements (`APC` *enables* `APC tourism`). This is the basis of the layering view.

The website does not replace the classroom document. The A–Z PDF (including the Quick-Reference sheet) remains a *generated release artifact* of the same data, so the Zenodo chain and the teaching sheet persist even as the site grows.

## 2. Audiences

| Audience | What they need |
| --- | --- |
| Bachelor's students in the seminar (any discipline) | Plain-language definitions readable before a session; the Quick-Reference for skimming |
| Students writing a term paper | Citable references (APA/BibTeX, DOI) per term; the layering view to connect concepts across themes |
| Teachers at other universities (OER reuse) | Stable URLs, per-term citation, downloadable data, licence clarity |
| Humanities / cultural anthropology researchers | Definitions grounded in their publishing reality (monographs, BPCs, GLAM, regional journals), not only STEM examples |
| GLAM and citizen-science practitioners | Entries on IIIF, crowdsourcing, infrastructuring written for non-computational readers |
| Future contributors (students in later semesters, community) | A workflow with issue forms, reviewable PRs, no programming knowledge required |
| Machines | SKOS, JSON-LD, CSV exports with persistent identifiers |

## 3. User stories

1. *Before session 1 (Publishing models)*: a student opens the site, selects the theme **Publishing models & economics**, and sees all related terms with one-line definitions; clicking through, they read APC, Gold/Green/Diamond/Hybrid OA as a connected set.
2. *Writing an essay*: a student layers **Publishing models & economics** + **Global equity & epistemic justice**, and traces the chain APC → APC tourism → Transformative agreement → Epistemic injustice → Diamond OA, with each link labelled ("APCs enable APC tourism", "Diamond OA responds to epistemic injustice").
3. *No-JavaScript / screen-reader user*: the same chain is available as a plain HTML table (relation, direction, partner term, one-line reason). Everything readable without JS.
4. *Citing*: a student copies an APA or BibTeX citation from the term page; the citation contains the permanent URL and the release DOI.
5. *Contributing*: a student in a later semester uses the "Suggest a term" issue form; the maintainer turns it into a term file via a reviewed pull request; the student appears as contributor with ORCID.
6. *Reusing*: a researcher downloads the full vocabulary as SKOS/Turtle (or CSV) and links it to their own grading-reform work without scraping HTML.
7. *German reader*: a reader switching to German sees translated labels/definitions where they exist, with graceful English fallback elsewhere.
8. *Maintainer handover*: a successor can take over within one working session using GOVERNANCE.md, the maintenance checklist, and the rebuild instructions.

## 4. The layering interaction

**Data basis.** Every term carries one or more themes. Every relation states a *type* from a small closed list (see [DATA-MODEL.md](DATA-MODEL.md), e.g. `enables`, `constrains`, `responds-to`, `contrasts-with`, `contributes-to`, `is-part-of`, `is-measured-by`, `related`) plus a short human sentence explaining it. The full relation list is curated, not crowdsourced.

**What layering does.** When a reader selects one or more themes, the site restricts the graph to terms tagged with *any* selected theme and shows the relations among them. Nodes and edges are the same data as the term pages; nothing is drawn that is not curated. The visual rendering (SVG at build time, optional JS enhancement) is only a different projection of that data.

### Worked example 1: Publishing economics × Global equity (the seminar's core equity story)

Selecting *Publishing models & economics* + *Global equity & epistemic justice* surfaces (among others):

| Edge | Grounded in |
| --- | --- |
| APC --enables--> APC tourism | APC entry: institutions' transformative-agreement coverage lets well-funded researchers publish OA, "while researchers at less well-funded institutions ... are left to pay full APCs" |
| Transformative agreement --enables--> APC tourism | TA entry: TAs "concentrate OA publishing benefits in well-resourced institutions, reinforcing inequities" |
| APC tourism --contributes-to--> Epistemic injustice | APC tourism entry: OA funding models "can reinforce rather than reduce global inequities" |
| Epistemic injustice <-- responds-to -- Diamond OA | Diamond OA entry: "the most equitable OA model for researchers globally" |
| Bibliodiversity <-- is-part-of -- SciELO, Redalyc, CLACSO | Bibliodiversity entry: used "to justify supporting SciELO, Redalyc, CLACSO" |

A student can now literally *see* the argument of the equity session: the same mechanism (APC-funded openness) that opens access in one place closes it elsewhere, and the response (Diamond OA, bibliodiversity, regional infrastructure) is itself an infrastructural choice.

### Worked example 2: Policy & mandates × Publishing economics

Selecting *Policy, mandates & rights* + *Publishing models & economics* surfaces the Green OA obstacle course:

```text
Embargo period --constrains--> Green OA
  (publisher-imposed delay before deposit is permitted)
Secondary publication right --constrains--> Embargo period
  (§38 UrhG: deposit after 12 months regardless of contract)
Accepted Manuscript --is-part-of--> Green OA
  (the version authors may usually self-archive)
Plan S --constrains--> Embargo period
  (no embargo permitted for funded research)
```

This layer answers the practical student question "what am I actually allowed to self-archive, and who says so?" by separating the mechanism (green route), the constraint (embargo), the legal counterweight (secondary publication right), and the funder mandate (Plan S).

### Worked example 3: Research integrity × Peer review

Selecting *Research integrity & reproducibility* + *Peer review* surfaces the reform cluster:

```text
HARKing --contributes-to--> Replication crisis
P-hacking --contributes-to--> Replication crisis
Pre-registration --responds-to--> HARKing
Registered Reports --responds-to--> P-hacking
Science sleuths / PPPPR --responds-to--> Replication crisis   (post-publication correction)
Replication Games --responds-to--> Replication crisis
```

The layering shows *where each intervention bites*: pre-registration and Registered Reports act before data collection; sleuths and Replication Games act after publication.

## 5. Scope (v1 and ongoing)

- All current glossary content, migrated verbatim first, then expanded (see [DATA-MODEL.md](DATA-MODEL.md) for the full term/theme assignment).
- English first; German as first additional language; model supports further languages.
- Themes and a small closed relation vocabulary, both as plain data files.
- Term pages, A–Z index, theme pages, layer view (static SVG + accessible tables), search (JS enhancement over a complete HTML index).
- Standards exports: SKOS (Turtle/JSON-LD), plain JSON, CSV; schema.org `DefinedTerm` markup.
- Persistent identifiers: stable term slugs, w3id.org permanent URL layer, Zenodo concept + version DOIs, Software Heritage archival.
- Contribution workflow (issue forms, PR review), governance and handover documentation, student-contribution guide.
- Institutional neutrality (ADR-0009): the site, namespace, repository metadata and citations name no institution as host, publisher or affiliation; contributor affiliations are optional and per person.

## 6. Non-goals

- **Not an encyclopedia.** Definitions stay glossary-length; deep treatment belongs in readings, not term pages.
- **Not a wiki.** All changes go through review; there is no anonymous editing.
- **Not a bibliographic database.** Sources per term (with DOIs where available), not exhaustive literature lists.
- **Not a FORRT fork.** The FORRT Glossary ([Parsons et al. 2022](https://doi.org/10.1038/s41562-021-01269-4)) covers open scholarship broadly (250+ terms, community-written, psychology-centred, CC BY-NC-SA). This glossary differs in focus (cultural anthropology and humanities publishing realities; equity and infrastructure analysis; the layering view) and links to FORRT/Wikidata concepts via `skos:exactMatch`/`closeMatch` instead of importing definitions (see ADR-0005); also because FORRT's NC licence is incompatible with reuse under this project's CC BY.
- **Not a knowledge ontology.** Relations exist only between glossary terms, are curated, and are explained in one sentence each; the site does not claim formal logical semantics.
- **No accounts, tracking, comments, analytics-by-default**, no dynamic backend, no database.
- **Not a facts ticker.** Dated facts (Elsevier revenue, journal counts) carry their as-of date and source; they are corrected through the normal release cycle, not auto-refreshed.

## 7. Success criteria

1. Usable in the running semester's seminar: A–Z, themes, term pages with citations, no JS required.
2. A student can cite any term with a copyable, DOI-backed reference.
3. Adding a term, theme, relation type, or language touches only data files, never build code (acceptance test in ROADMAP Phase 1/3).
4. The site rebuilds identically with pinned tooling documented in one page (ADR-0002, docs/rebuild.md).
5. Every released version resolves through a DOI and a permanent URL independent of GitHub.
6. A successor maintainer can take over using documented governance and maintenance checklists.

## 8. Relation to existing work

- **FORRT Glossary** (verified: [Parsons et al. 2022, *Nature Human Behaviour* 6(3), 312–318](https://doi.org/10.1038/s41562-021-01269-4); glossary at [forrt.org/glossary](https://forrt.org/glossary); licence CC BY-NC-SA 4.0): positioned as complementary; per-term `skos:closeMatch` links planned (ADR-0005).
- **Wikidata**: per-term `skos:exactMatch` to Wikidata Q-IDs where a solid equivalent concept exists (added field in data model; filled incrementally).
- **UNESCO Recommendation on Open Science (2021)**: the glossary's stated grounding; cited as a source across entries; the vocabulary could later align its reading of open science taxonomy where overlap exists. (kept as-is from the source document's stated groundings; any restructuring is a later editorial decision)
- **Zenodo v1.0.0 record** ([10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750), version 1.0.0, published 2026-10-18, resource type "Lesson", CC BY 4.0): is the record of the whole glossary line: v2.0.0+ publishes as new versions of this same record, keeping one concept DOI from the Word edition onward (D-3, ADR-0004).
