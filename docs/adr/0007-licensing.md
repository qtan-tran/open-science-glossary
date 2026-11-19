# ADR-0007: Licensing and per-file-type licences

Status: proposed · Decides: content + code licences, font policy

## Context

The glossary itself teaches that licences shape reuse; the site must model that consistency. Content and code have different authorship and different reuse norms (scholarly sharing culture vs. code reuse with attribution).

## Options considered

1. **Everything CC BY 4.0.** Scholastically clean for prose; unusual and suboptimal for code (code under CC licences confuses: without a warranty clause, CC is not recommended for code).
2. **Everything MIT.** Wrong direction for prose: content is what students should reuse under scholarly norms.
3. **Split: content CC BY 4.0, code MIT.** Standard for content-plus-code scholarly projects. Chosen.

## Decision

1. **Content** (term files, data files, built pages, exports, docs): **CC BY 4.0**, stated in LICENSE-CONTENT, declared per release on Zenodo, in CITATION.cff, in the site footer, in each term page's citation partial.
2. **Code** (build scripts, layouts, workflows, schema, the small JS enhancement): **MIT**, stated in LICENSE-CODE. A short readme note explains the split so a downloader knows which applies to what.
3. **Fonts: no bundled fonts.** System font stacks only (also decided in ADR-0006); avoids font-licence laundering risk entirely (a documented failure mode in GLAM-adjacent projects when webfonts get re-hosted without licence attention).
4. External sources quoted in term entries are cited, never copied beyond quotation-right norms; FORRT text never copied (CC BY-NC-SA, per ADR-0005).

## Consequences

- Zero ambiguity at handover: a successor maintainer knows instantly what they may reuse, relicense-not, and how to attribute contributions.
- Student contributions are accepted under a simple line in the PR template / issue forms ("contributions are published under CC BY 4.0, with ORCID/name credit"), no CLA needed for a glossary; a lightweight document, no legal overhead.
- Downstream users (e.g. a lecturer wanting a printable excerpt) only need to attribute: the exact requirement CC BY itself mandates.
