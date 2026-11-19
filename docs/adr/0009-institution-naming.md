# ADR-0009: Institutional neutrality

Status: accepted 2026-11-19 (maintainer decision D-12) · Decides: institutional naming policy for site, metadata and citations

## Context

The glossary began as teaching material, but its intended lifetime (ten-plus years) exceeds any single course, employment or hosting arrangement. Naming a university as host, publisher or affiliation creates implied endorsement, complicates a future move between maintainers or hosts, and pollutes citation metadata with roles (publisher, host) that the project does not actually carry.

## Decision

1. The site, the repository metadata, the w3id namespace, the Zenodo record metadata and every generated citation name **no institution** (including Universität Hamburg) as host, publisher or affiliation of the project.
2. Exactly one permitted mention, a single factual origin line on the About page and in the v1.0.0 history: "Originally created for the course Introduction to Open Science, Universität Hamburg, Winter Semester 2026/27."
3. Contributor affiliations are **optional and per person** (front matter field "affiliation" on a contributor, never a project-wide field). They credit people; they never describe the project.
4. The w3id namespace (os-glossary) carries no institutional semantics (D-7), so the identifier layer survives any institutional change.

## Consequences

- The glossary can change maintainer, host or institutional context without touching identifiers, metadata or past citations.
- CITATION.cff and Zenodo metadata carry no institutional publisher field; authorship is carried by named contributors with ORCIDs.
- Course-based reuse in other universities inherits nothing to remove: the project is neutral by construction.
