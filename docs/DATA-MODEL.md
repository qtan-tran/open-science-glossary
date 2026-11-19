# DATA MODEL — Open Science Glossary website

Status: draft for review · Companion: [CONCEPT.md](CONCEPT.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ROADMAP.md](ROADMAP.md)

## 1. Principles

1. **Content is data** (ADR-0001): one plain-text file per term, editable in the GitHub web UI; controlled vocabularies in their own small files; the whole repository readable and reusable without the website.
2. **Everything validated** (this file's schemas + scripts/validate.py): a broken cross-reference fails CI.
3. **Identity is permanent** (ADR-0003): the id/slug is the term's identity; labels can change, slugs cannot be reused.
4. **Language is a layer, not a fork**: translations are per-term sibling files sharing the id.

## 2. Entity overview

| Entity | What it is | Where it lives | Identity |
| --- | --- | --- | --- |
| Term | A glossary entry | content/terms/<id>.md (+ <id>.<lang>.md translations) | slug |
| Theme | A teaching/topic layer over terms | data/themes.yaml | short id (equity) |
| Relation type | A closed vocabulary of directed relations | data/relationship-types.yaml | id (enables) |
| Edge | A typed relation between two terms | related: list in term front matter | (source id, type, target id) |
| Language | UI + content language | data/languages.yaml | ISO code (en, de) |
| Release | A tagged, citable snapshot of all content | git tag + Zenodo version | semver + DOI |

## 3. Term file specification

### 3.1 Front matter (structured metadata)

| Field | Type | Required | Meaning / rules |
| --- | --- | --- | --- |
| id | string | yes | slug: lowercase, hyphens; once assigned never changed, never reused |
| title | string | yes | current human label (may change any time) |
| alternatives | array | no | abbreviations, synonyms; exported as skos:altLabel (e.g. "Author Accepted Manuscript" on accepted-manuscript) |
| themes | array | yes | 1 + ids from data/themes.yaml; first entry = primary theme |
| status | enum | yes | draft / reviewed; deprecated requires replaced_by |
| replaced_by | slug or null | if deprecated | successor term; page stays, redirects visually |
| date_created | date | yes | date the term entered the glossary (migrated terms: 2026-10-18, the v1.0.0 record date) |
| date_last_changed | date | yes | last substantive change (not typo fixes) |
| sources | array | yes (at least 1) | each: text + optional doi/url; DOI preferred where available |
| contributors | array | yes | each: name, optional orcid, role (author/reviewer/translator/editor) |
| related | array | no | typed edges, see section 5 |
| matches | object | no | wikidata (Q-ID), forrt (slug/URL) for external alignment (ADR-0005) |

lang is implicit from the filename (see section 6), never hand-edited.

### 3.2 Body conventions (parsed by the build, enforced by validate)

```text
1st paragraph            -> the definition (also skos:definition, schema:description; max ~120 words)
## Details               -> bullet points (each rendered as-is)
> [!WARNING] blockquote  -> the common misconception (distinct styling; max 1 per term)
anything else            -> validation error
```

GitHub renders these conventions naturally (alert blockquotes, headings), so the files are *already* readable in the repo without any site. Migrated v1.0.0 "See also" lists are stored as related entries of type related (untyped links), then progressively typed during Phase 2 curation.

### 3.3 Fully worked example: content/terms/apc.md

```markdown
---
id: apc
title: APC (Article Processing Charge)
alternatives:
  - Article Processing Charge
themes:
  - publishing
  - equity
status: reviewed
date_created: 2026-10-18
date_last_changed: 2026-10-18
contributors:
  - name: Quoc-Tan Tran
    orcid: 0000-0003-3533-5858
    role: author
sources:
  - text: UNESCO Recommendation on Open Science (2021)
  - text: cOAlition S, Plan S principles
    url: https://www.coalition-s.org/
related:
  - type: related
    target: bpc
  - type: related
    target: diamond-oa
  - type: related
    target: gold-oa
  - type: related
    target: hybrid-oa
  - type: related
    target: plan-s
  - type: related
    target: apc-waiver
  # Phase 2 curation adds, among others:
  # - type: enables, target: apc-tourism, reason: "Institutions whose transformative
  #   agreements cover APCs let their researchers publish OA at no personal cost,
  #   while others pay full APCs or seek waivers."
---

A fee paid by an author (or their institution or funder) to a journal so that an
article is made immediately and permanently open access on the publisher's website.

## Details

- Typical range: EUR 500 - 11,000+ depending on publisher and journal prestige
- APCs shift publishing costs from the reader to the author, which can exclude
  researchers from lower-income institutions or countries
- Not to be confused with BPC (Book Processing Charge), which applies to monographs

> [!WARNING]
> Paying an APC does not guarantee publication; it only funds open access after
> acceptance.
```

### 3.4 Translation example: content/terms/apc.de.md (Phase 5)

```markdown
---
id: apc
title: APC (Verarbeitungsgebühr je Artikel)
themes:
  - publishing
  - equity
contributors:
  - name: (translator, ORCID)
    role: translator
status: reviewed
---

Eine Gebühr, die Autor:innen (oder ihre Institution oder Fördergeber:innen) an
eine Zeitschrift zahlen, damit ein Artikel unmittelbar und dauerhaft frei
zugänglich auf der Verlagswebsite veröffentlicht wird.

## Details

...
```

Rules: translations repeat only the fields that differ locally (title, related prose); the build merges by id. Missing translations fall back to English with a visible notice (graceful degradation, no broken pages). Sources and edge *types* are shared (they live on the concept); edge reason sentences may be translated by overriding the edge in the translation file.

### 3.5 Deprecation example (hypothetical shape)

```markdown
---
id: platinum-oa
title: Platinum OA
status: deprecated
replaced_by: diamond-oa
themes:
  - publishing
date_created: 2026-10-18
date_last_changed: 2028-03-01
---

"Platinum OA" is an older label for the model this glossary now treats under
Diamond OA (see that entry).
```

Deprecated pages always resolve (ADR-0003), visibly point to the successor, and are excluded from counts; in exports they carry a deprecation annotation and the successor link. The Diamond OA entry already notes "Platinum OA" as an alternative label, so this page exists only as an illustrative shape: it would be created if an alias or split term ever needed a permanent home.

## 4. Controlled vocabularies

### 4.1 data/themes.yaml (11 themes, the teaching layers)

| id | Label | Description (draft) |
| --- | --- | --- |
| publishing | Publishing models & economics | How research outputs get published, who pays, and with what consequences |
| policy | Policy, mandates & rights | Funder requirements, declarations, laws, and author rights |
| assessment | Research assessment & metrics | How quality and impact are measured, and how they are misused |
| integrity | Research integrity & reproducibility | Practices, failures, and reforms that make findings trustworthy |
| infrastructure | Infrastructure, platforms & identifiers | Repositories, registries, software and services underlying research |
| data | Research data & governance | FAIR/CARE, data management planning, data stewardship |
| peer-review | Peer review | The refereeing system and its open reform variants |
| participation | Participation & public engagement | Citizen science, crowdsourcing, co-production with communities |
| heritage | Cultural heritage & GLAM | Galleries, libraries, archives, museums, digitisation, reuse |
| equity | Global equity & epistemic justice | Who is structurally included or excluded as a knower |
| licensing | Licensing & copyright | Open licences, waivers, rights retention |

(The draft taxonomy in the planning request revived "Cultural heritage & GLAM" and added "Licensing"; 11 themes sit within the 8-12 target. Themes remain open to revision in review; assignment changes are logged as patches, new themes as minor releases.)

### 4.2 data/relationship-types.yaml (closed list of 8)

| id | Meaning (source -> target) | SKOS export | Example (real, from current content) |
| --- | --- | --- | --- |
| is-part-of | target contains/is the broader frame of source | skos:broader | "Accepted Manuscript is-part-of Green OA route" |
| enables | source makes target possible or much easier | osg:enables (subPropertyOf skos:related) | "APC enables APC tourism" |
| constrains | source limits, delays or burdens target | osg:constrains | "Embargo Period constrains Green OA" |
| responds-to | source is a reform/remedy directed at target's problem | osg:respondsTo | "Diamond OA responds-to Epistemic Injustice" |
| contributes-to | source is a documented driver of target | osg:contributesTo | "HARKing contributes-to Replication Crisis" |
| contrasts-with | commonly confused or meaningfully opposite pair | osg:contrastsWith | "Replication contrasts-with Reproducibility" |
| is-measured-by | source is quantified/captured by target | osg:isMeasuredBy | "Researcher career impact is-measured-by H-index" (planned entry) |
| related | untyped cross-reference (fallback, pre-curation default) | skos:related | all migrated "See also" pointers |

Rules: every edge is entered *once*, on the curatorial subject term; the build generates the inverse view automatically ("enabled by", "constrained by", ...). A reason sentence is required for every type except related. is-part-of may never be cyclic; contrasts-with renders symmetrically but is stored once.

## 5. Draft JSON Schema (front matter)

This is the draft to be finalized as schemas/term.schema.json in Phase 0. It validates what YAML front matter becomes after parsing.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://w3id.org/os-glossary/schema/term.schema.json",
  "title": "Open Science Glossary term (front matter)",
  "type": "object",
  "required": ["id", "title", "themes", "status", "date_created", "date_last_changed", "sources", "contributors"],
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
      "description": "Stable slug; never changed, never reused (ADR-0003)"
    },
    "title": { "type": "string" },
    "alternatives": { "type": "array", "items": { "type": "string" } },
    "themes": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "string",
        "enum": ["publishing", "policy", "assessment", "integrity", "infrastructure",
                 "data", "peer-review", "participation", "heritage", "equity", "licensing"]
      }
    },
    "status": { "type": "string", "enum": ["draft", "reviewed", "deprecated"] },
    "replaced_by": {
      "type": ["string", "null"],
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
    },
    "date_created": { "type": "string", "format": "date" },
    "date_last_changed": { "type": "string", "format": "date" },
    "sources": { "type": "array", "minItems": 1, "items": { "$ref": "#/definitions/source" } },
    "contributors": { "type": "array", "minItems": 1, "items": { "$ref": "#/definitions/contributor" } },
    "related": { "type": "array", "items": { "$ref": "#/definitions/relation" } },
    "matches": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "wikidata": { "type": "string", "pattern": "^Q[0-9]+$" },
        "forrt": { "type": "string" }
      }
    }
  },
  "definitions": {
    "source": {
      "type": "object",
      "required": ["text"],
      "additionalProperties": false,
      "properties": {
        "text": { "type": "string" },
        "doi": { "type": "string", "pattern": "^10\\..+" },
        "url": { "type": "string", "format": "uri" }
      }
    },
    "contributor": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string" },
        "orcid": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$" },
        "role": { "type": "string", "enum": ["author", "reviewer", "translator", "editor"] }
      }
    },
    "relation": {
      "type": "object",
      "required": ["type", "target"],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "enum": ["is-part-of", "enables", "constrains", "responds-to",
                   "contributes-to", "contrasts-with", "is-measured-by", "related"]
        },
        "target": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$" },
        "reason": { "type": "string", "description": "One sentence; required for every type except related" }
      }
    }
  }
}
```

Validation additionally enforces (in scripts/validate.py, beyond what JSON Schema can express): every related.target is an existing term id or listed in data/candidates.yaml; deprecated implies replaced_by pointing at a live term; contrasts-with/related pairs are not entered on both ends; body conventions (3.2) hold; themes used match data/themes.yaml.

## 6. Languages

| Rule | Detail |
| --- | --- |
| File naming | content/terms/<id>.md = English; content/terms/<id>.de.md = German; new languages = new suffix, no code changes |
| data/languages.yaml | maps ISO code to UI strings (language name, "not yet translated" notice) |
| Fallback | missing translation -> English content rendered under the DE URL with a visible notice |
| Exports | SKOS prefLabel@de etc. per available translation; CSV gains a lang column per (term, language) row |
| Citation | the translated term page cites the same release DOI; translations are part of the same version |

## 7. Current content: assignment of every existing term to themes

Draft assignment of the v1.0.0 document (to be confirmed during migration, ROADMAP 0.4/0.5). Primary theme first. Combined headings are marked; the recommended splits (OPEN-QUESTIONS Q4) yield separate rows.

| # | Heading (v1.0.0) | Slug (draft) | Themes (primary, additional) | Note |
| --- | --- | --- | --- | --- |
| 1 | APC (Article Processing Charge) | apc | publishing, equity | |
| 2 | APC Waiver | apc-waiver | publishing, equity | |
| 3 | APC Tourism | apc-tourism | equity, publishing | |
| 4 | Accepted Manuscript (AM) | accepted-manuscript | publishing, licensing | alt label AAM |
| 5 | Barcelona Declaration | barcelona-declaration | policy, infrastructure | |
| 6 | Bibliodiversity | bibliodiversity | equity, publishing | |
| 7 | BPC (Book Processing Charge) | bpc | publishing, equity | |
| 8 | CARE Principles | care-principles | data, equity | |
| 9 | CC0 | cc0 | licensing, heritage | |
| 10 | CC BY | cc-by | licensing, publishing | |
| 11 | Citizen Science / Citizen Humanities | citizen-science | participation, heritage | |
| 12 | CLACSO | clacso | equity, publishing, infrastructure | |
| 13 | CoARA | coara | assessment, policy | |
| 14 | Co-production (of knowledge) | co-production | participation, equity | |
| 15 | CrossRef | crossref | infrastructure | |
| 16 | Crowdsourcing (in research) | crowdsourcing | participation, heritage | |
| 17 | DataCite | datacite | infrastructure, data | |
| 18 | Diamond OA | diamond-oa | publishing, equity, infrastructure | |
| 19 | DMP (Data Management Plan) | dmp | data, policy | |
| 20 | DOI | doi | infrastructure | |
| 21 | DORA | dora | assessment, policy | |
| 22 | Elsevier | elsevier | publishing, policy | |
| 23 | Embargo Period | embargo-period | publishing, policy | |
| 24 | Epistemic Injustice | epistemic-injustice | equity, participation | |
| 25 | FAIR Principles | fair-principles | data, infrastructure | |
| 26 | GLAM | glam | heritage, participation | |
| 27 | Gold OA | gold-oa | publishing | |
| 28 | Green OA | green-oa | publishing, policy | |
| 29 | HARKing | harking | integrity | |
| 30 | H-index | h-index | assessment | |
| 31 | Hybrid OA | hybrid-oa | publishing, policy | |
| 32 | IIIF | iiif | heritage, infrastructure | |
| 33 | Impact Factor (JIF) | impact-factor | assessment | |
| 34 | Infrastructuring | infrastructuring | heritage, participation, infrastructure | |
| 35 | OA (Open Access) | open-access | publishing | umbrella entry |
| 36 | OJS | ojs | infrastructure, publishing | |
| 37 | OMP | omp | infrastructure, publishing | |
| 38 | Open Peer Review | open-peer-review | peer-review | |
| 39 | ORCID | orcid | infrastructure | |
| 40 | Paper Mill | paper-mill | integrity, publishing | |
| 41 | P-hacking | p-hacking | integrity | |
| 42 | PID (Persistent Identifier) | pid | infrastructure | umbrella entry |
| 43 | Plan S | plan-s | policy, publishing | |
| 44 | Predatory Journal | predatory-journal | integrity, publishing | |
| 45 | Pre-print | preprint | publishing, infrastructure | |
| 46 | Pre-registration | pre-registration | integrity | |
| 47 | Read-and-Publish Agreement (Transformative Agreement) | transformative-agreement | publishing, policy, equity | combined heading, single concept (Q4) |
| 48 | Redalyc | redalyc | equity, publishing, infrastructure | |
| 49 | Registered Reports | registered-reports | integrity, peer-review | |
| 50 | Replication / Reproducibility | reproducibility + replication | integrity (both) | combined heading; split recommended (Q4), contrasts-with edge |
| 51 | Replication Crisis | replication-crisis | integrity, assessment | |
| 52 | Replication Games | replication-games | integrity, participation | |
| 53 | Repository | repository | infrastructure, data | |
| 54 | ROR | ror | infrastructure | |
| 55 | Salami Slicing | salami-slicing | integrity, assessment | |
| 56 | Science Sleuths / Post-Publication Peer Review | science-sleuths + post-publication-peer-review | peer-review, integrity (both) | combined heading; split recommended (Q4) |
| 57 | SciELO | scielo | equity, publishing, infrastructure | |
| 58 | Secondary Publication Right | secondary-publication-right | policy, licensing | |
| 59 | SHERPA/RoMEO | sherpa-romeo | infrastructure, publishing | |
| 60 | Springer Nature | springer-nature | publishing | |
| 61 | Version of Record (VoR) | version-of-record | publishing, licensing | |
| 62 | Wikimedia Commons | wikimedia-commons | heritage, participation, infrastructure | |
| 63 | Zenodo | zenodo | infrastructure, data | |
| 64 | Zooniverse | zooniverse | participation, heritage | |
| 65 | DOAJ (Quick-Reference only, no entry in v1.0.0) | doaj | publishing, infrastructure | new term candidate (Q5) |

### 7.1 Count reconciliation (blocking for migration, see OPEN-QUESTIONS Q11)

The Zenodo record and course description say "55 core terms"; the structured extraction of the source document yields **64 A-Z headings**, three of which are combined pairs (rows 47, 50, 56), plus one Quick-Reference-only term (DOAJ). With all recommended splits and DOAJ added, the launch set is 67 term files. The migration acceptance test (ROADMAP 0.4) enumerates every heading programmatically and cross-checks against the maintainer's own list, so neither "55" nor "64" is silently trusted.

### 7.2 Dangling references (candidate terms referenced but not yet defined)

The v1.0.0 body and see-also lists reference the following concepts that have no entry yet. They live in data/candidates.yaml (valid link targets, but unlinked until real entries exist). Suggested first batch (OPEN-QUESTIONS Q5): Open Data, cOAlition S, Serials Crisis, Publication Bias, DOAJ, Altmetrics, PKP, Open Access Monograph, Retraction Watch, PubPeer.

Full list: Altmetrics; arXiv; Bibliometrics; cOAlition S; Community Archive; Digital Heritage; Indigenous Data Sovereignty; Open Access Monograph; Open Cultural Heritage; Open Data; OSF (Open Science Framework); PKP (Public Knowledge Project); Publication Bias; PubPeer; Participatory Research; Retraction Watch; SocArXiv; Think-Check-Submit; Wiki Goes MEK; WikiSource; Wikipedia; ISBN/ISSN (mentioned under PID); RRID (mentioned under PID). All are real, well-documented concepts (each to be verified against its own sources during the writing pass, ROADMAP Phase 4 backlog), defined with their own sources before linking switches on.

## 8. Versions and releases (data-facing summary; policy in ADR-0004)

- Glossary releases are semver; the data carries per-term dates that drive the generated CHANGELOG.
- Each release freezes: source ZIP (Zenodo), built site + exports (release assets, ADR-0004), SKOS/CSV/JSON snapshots, and this data model's version.
- Schema evolution: this schema is versioned with the same releases; additive changes (new optional fields) are minor; breaking changes (renamed/removed fields) are major with a documented migration in the CHANGELOG.
- Every term page and export carries the release it belongs to, enabling "state of term X at v2.1.0" questions to be answered from Zenodo/SWH archives alone.
