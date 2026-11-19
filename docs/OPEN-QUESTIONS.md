# OPEN QUESTIONS — decisions only the maintainer can make

Each item carries a recommendation. Nothing blocks on these except Q1/Q2 before Phase 0/1 implementation starts.

## Q1. The repo is currently empty. Where do the v1.0.0 sources live?
qtan-tran/open-science-glossary had no commits when this planning started (a placeholder README on main and this branch were created to open this PR). legacy/build_glossary.js (mentioned in the original plan) does not exist there yet. ROADMAP Phase 0 assumes the published v1.0.0 PDF (from the [Zenodo record](https://doi.org/10.5281/zenodo.23449750)) and the original DOCX are committed under legacy/ as the frozen input for migration.
**Recommendation:** commit OpenScience_Glossary.pdf (the exact file of record 10.5281/zenodo.23449750), the source DOCX, and any earlier JS/Word tooling to legacy/ in the first repo-seeding commit.

## Q2. Static site generator: Hugo (recommended) or Eleventy?
ADR-0002 argues Hugo (single binary, native taxonomies = themes, native multilingual = translation files). Eleventy is the runner-up if you strongly prefer a JavaScript codebase you can hack on yourself.
**Recommendation:** Hugo.

## Q3. Version numbering for the first site release: v2.0.0 (recommended) or v1.1.0?
The data model restructures the glossary (one file per term, new metadata), which is a major re-definition of the artefact's form, not an addition.
**Recommendation:** tag the first site release v2.0.0 and treat the v1.x line as the PDF era; this also aligns with the new Zenodo record (ADR-0004).

## Q4. Term granularity: split the three combined entries?
The document has three combined headings: "Replication / Reproducibility", "Science Sleuths / PPPPR", and "Read-and-Publish Agreement (Transformative Agreement)". Splitting Replication vs Reproducibility into two pages connected by a contrasts-with edge directly supports the layering view and matches how the seminar teaches the distinction. "Transformative Agreement" is genuinely one concept (one term, two labels). Science Sleuths are actors, PPPPR is a practice; two pages linked by a plain related edge would be cleaner without needing a new relation type.
**Recommendation:** split into two pages each for Replication/Reproducibility and Science Sleuths/PPPR (counted as part of the v2.0.0 baseline, not as later minor releases); a single page for Transformative Agreement with both labels.

## Q5. Which missing/dangling references should exist before the semester starts?
The v1.0.0 text cross-references terms that have no entry yet (they would break reference checks at migration): see the full list in DATA-MODEL section 7.2, plus DOAJ, which appears in the Quick-Reference with no entry. Creating empty stubs for all of them is worse (empty pages) than picking a first batch.
**Recommendation:** define all dangling references in data/candidates.yaml (the build lists them without linking), and write full entries in this priority order for v2.1.0 (after the semester, not before): Open Data, cOAlition S, Serials Crisis, Publication Bias, DOAJ, Altmetrics, PKP, Open Access Monograph, Retraction Watch, PubPeer.

## Q6. Per-term citability: URL + version DOI (recommended) vs per-term DOIs
Minting a DOI per term (60+ now, growing) would need a DataCite account/agency or per-term Zenodo deposits; that is real work per release for limited citation benefit, since glossary entries change between versions.
**Recommendation:** each term page shows copyable APA + BibTeX citing the *term within the versioned glossary* via its w3id permanent URL plus the release version DOI (and the concept DOI), as decided in ADR-0004; revisit only if a concrete use case emerges.

## Q7. w3id namespace string
https://w3id.org/os-glossary/... is short and descriptive. Alternatives: /open-science-glossary/ (long, but unambiguous), /glossary/ (too generic; the w3id admins may deny overly generic names, per their naming policy).
**Recommendation:** os-glossary; register the .htaccess once Phase 1's URL structure exists so there is something live to redirect to.

## Q8. Hosting timing
GitHub Pages now (ADR-0008) vs asking UHH for a static directory / a uni subdomain redirect from day one.
**Recommendation:** GitHub Pages immediately; consider a UHH move only if institutional branding becomes a requirement (the w3id layer makes the move cost-free to readers).

## Q9. German translations scope (Phase 5)
All terms is the end state; the first student cohort could translate a pilot batch (e.g. the publishing + policy core used in the first sessions) as course activity.
**Recommendation:** a pilot batch of about 12 high-traffic terms reviewed by a German-language reader before expanding; per-term .de.md files (DATA-MODEL) mean no redesign later.

## Q10. Governance timing
GOVERNANCE.md in Phase 0 (minimal: maintainer decides, contributors credited, successor process) vs deferring to Phase 4 (community workflow).
**Recommendation:** the minimal version now (Phase 0); it doubles as handover documentation if anything happens to you before Phase 4 lands.

## Q11. Raw term count reconciliation
The Zenodo record and course material describe "55 core terms"; the structured extraction of the DOCX yields 64 A-Z headings (three of which are combined pairs) plus one Quick-Reference-only term (DOAJ). The difference is probably a counting basis issue, but only you can confirm.
**Recommendation:** treat this as the Phase 0 acceptance test: scripted extraction from legacy/ must enumerate every heading and cross-check it against your own expected list, so "nothing was lost" and "nothing half-migrated" are both provable; correct the README/Zenodo description numbers in the first release.
