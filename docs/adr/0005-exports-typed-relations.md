# ADR-0005: Exports, SKOS mapping, typed relationships, schema.org

Status: proposed · Decides: interoperability formats, relation vocabulary, ontology mapping

## Context

The glossary's value compounds if it interops with the scholarly web: library and terminology tools (SKOS), spreadsheets (CSV), developers (JSON), search engines (schema.org), and the existing ecosystem of glossaries (Wikidata, FORRT per Parsons et al. 2022, Nature Human Behaviour, doi:10.1038/s41562-021-01269-4). v1.0.0 has none of these. FORRT is CC BY-NC-SA: we can never copy their text into this CC BY 4.0 glossary, only link.

## Options considered

1. **Full custom RDF vocabulary** (own ontology): rejected; overkill for a glossary and a hallmark of overengineering.
2. **SKOS only, relying on skos:related for all relations**: insufficient, loses the interaction semantics at the core of this project.
3. **Typed closed set of relations, mapped to SKOS + schema.org light: chosen.**

## Decision

1. **Typed relations (closed set of 8)**, each machine-checked, each with rdfs:subPropertyOf mapping for export so generic SKOS consumers still work:

| Relation | SKOS fallback |
| --- | --- |
| is-part-of | skos:broader |
| enables | subProperty of skos:related, own IRI osg:enables |
| constrains | subProperty of skos:related, own IRI osg:constrains |
| responds-to | subProperty of skos:related, own IRI osg:respondsTo |
| contributes-to | subProperty of skos:related, own IRI osg:contributesTo |
| contrasts-with | subProperty of skos:related, own IRI osg:contrastsWith |
| is-measured-by | subProperty of skos:related, own IRI osg:isMeasuredBy |
| related | skos:related |

   Namespace osg: = https://w3id.org/os-glossary/vocab/ (redirects to a small vocabulary page). Relations on term pages always carry a human-readable reason, so the network view is pedagogically meaningful.

2. **SKOS export via rdflib** (Python): one ConceptScheme = the glossary; each term = skos:Concept with skos:definition, skos:altLabel (abbreviations, e.g. "APC"), language-tagged prefLabel (en now, de when the German translation exists); themes = skos:Collection instances. Published as Turtle + JSON-LD alongside each release.

3. **JSON + CSV exports** for non-specialists (CSV: term, definition, themes, relations flattened; per-language columns), generated from the data files, never hand-maintained.

4. **schema.org DefinedTerm / DefinedTermSet JSON-LD** embedded in each term page and the glossary root; terms link to their permanent URLs (ADR-0003) as url and to the release via isPartOf -> DefinedTermSet with the Zenodo version DOI.

5. **External mappings, per term, optional fields:**
   - matches.wikidata: skos:exactMatch to the entity's URI (used sparingly; only when Wikidata covers the same concept, else omitted)
   - matches.forrt: skos:closeMatch to the FORRT glossary entry. Their CC BY-NC-SA means we never copy their text, only link.

6. Where no exact equivalent exists (several of our humanities/equity terms), no mapping: absence is better than a wrong link.

## Consequences

- Cost: one Python export script, one schema update, two optional front-matter fields.
- Bibliodiversity intact; no vendor lock; each export is generated, never hand-edited (single source of truth, ADR-0001).
