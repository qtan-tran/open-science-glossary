# ROADMAP — Open Science Glossary website

Status: draft for review · Effort units: **S** = one focused working session (up to 2h), **M** = half a day.
MARKER blocks: **[TB]** = teaching blocker: steps that must be finished before the glossary is first assigned to students in the running Winter Semester.

Only phases 0 and 1 are teaching blockers, plus 2.1 (relation *data*, because the equity-session chain is the site's pedagogical core). Everything else can slip a semester without harm.

## Phase 0 — Foundations

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 [TB] | Seed repo | Put the frozen sources in version control | Commit the v1.0.0 PDF (identical to the Zenodo record), the source DOCX, and any old build tooling under legacy/; init README.md, LICENSE-CONTENT (CC BY 4.0), LICENSE-CODE (MIT), minimal GOVERNANCE.md (ADR-0007, OPEN-QUESTIONS Q10) | legacy/ holds a byte-identical v1.0.0 PDF (md5 check vs Zenodo); licences displayed on the repo landing page | S | No |
| 0.2 | Scaffold data model | Controlled vocabularies live as data | Write data/themes.yaml (11 themes per DATA-MODEL), data/relationship-types.yaml (8 types), data/languages.yaml, data/candidates.yaml (dangling refs list) | data/* | files parse; ids match DATA-MODEL |
| 0.3 | Schema | Validation exists before content migrates | Write schemas/term.schema.json + schemas/vocabulary.schema.json; scripts/validate.py (front matter schema, unknown theme/relation/target checks); pinned requirements.txt | schemas/*, scripts/validate.py | validate.py correctly rejects a deliberately broken sample term (smoke test) and accepts a valid one |
| 0.4 [TB] | Migration | 1:1 extraction of v1.0.0 into term files | Script (or semi-manual conversion) from legacy/OpenScience_Glossary.docx to content/terms/*.md per DATA-MODEL spec (front matter minimum: id, title, themes, dates, status, sources, contributors), body conventions preserved (definition / details / warning / see-also as related) | content/terms/* | every heading extracted (count reconciliation, OPEN-QUESTIONS Q11: programmatically enumerated and cross-checked against the maintainer's own list); every see-also target resolves or is in candidates.yaml; 10 random terms spot-checked by eye against the DOCX |
| 0.5 [TB] | Theme assignment | Every migrated term mapped | Apply the theme table of DATA-MODEL (drafted there; confirm while migrating) | content/terms/* | validate passes with themes required |
| 0.6 [TB] | CI hygiene | The repo enforces its own rules | .github/workflows/validate.yml; branch protection; CITATION.cff (v1 lineage; concept DOI of the new Zenodo record filled after first release; OPEN-QUESTIONS Q3, ADR-0004); .zenodo.json with a related identifier pointing to 10.5281/zenodo.23449750 | .github/*, CITATION.cff, .zenodo.json | a red PR is blocked, a green one merges; the CFF passes a cff validation check |

## Phase 1 — Minimum citable site

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 [TB] | Site skeleton | Hugo builds terms into pages | Hugo site with pinned version; layouts: term page (definition, details, warning, relationships), A-Z index, theme pages; system font stack, semantic HTML, skip link | layouts/*, assets/*, site config | hugo builds locally with zero warnings; all term pages reachable; one small CSS file only |
| 1.2 [TB] | No-JS reading core | Core reading complete without JS | One "all terms" page (headings + one-line definitions) + per-theme pages; browser in-page search is the JS-off search | layouts | JS-disabled walkthrough: any term findable, every cross-link works |
| 1.3 [TB] | Term citations | Every term citable | APA + BibTeX partial on term pages (release-versioned placeholder until the first DOI mints); footer with whole-glossary citation | layouts partial | copy from page -> BibTeX entry parses (generated bib compiles in a CI smoke test) |
| 1.4 [TB] | Deploy | Public site online | deploy.yml: build -> GitHub Pages; Codeberg mirror push job (ADR-0008) | .github/workflows/deploy.yml | live URL serves the built site; local build diff vs served page matches |
| 1.5 | Permanent URLs | Citability independent of host | Fork perma-id/w3id.org; add ids/os-glossary/.htaccess per ADR-0003 (rules tested); open PR upstream | (upstream repo) | curl -sIL https://w3id.org/os-glossary/term/apc returns 302 then 200 | S (plus upstream merge wait) | Can slip past semester start: cite the GitHub Pages URL until merged, switch printed material afterwards |
| 1.6 [TB] | First release v2.0.0 | The DOI chain exists | Enable the Zenodo integration (sandbox test first, per Zenodo docs); tag v2.0.0; verify concept + version DOIs; edit the old record's metadata to link the successor; README badges | tag, CHANGELOG.md (generated) | Zenodo shows correct metadata from CITATION.cff/.zenodo.json; concept DOI resolves to latest; both records cross-link | S | No |
| 1.7 | Rebuild doc | Abandonment insurance written early | docs/rebuild.md: pinned tools, local build steps, migration story if Hugo dies | docs/rebuild.md | a colleague with no context can follow it | S | Yes, but strongly recommended |

## Phase 2 — Relationships and layering

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 [TB for content] | Relation data | Typed relations curated | Add curated relations (start with the three CONCEPT worked examples; 40-60 edges total) with one-line reasons, real entries only | content/terms/* | validate passes; the three CONCEPT chains render fully | M | The chains needed for the semester's sessions: no |
| 2.2 | Relationships table UI | Canonical accessible view | Term pages render the Relationships table (relation, direction, partner, reason) | layouts | table readable in a screen-reader spot test; all edges visible bidirectionally | S | No |
| 2.3 | Layer pages (static) | Theme-combination views | scripts/build_layers.py produces per-theme-pair pages: filtered term list + SVG (deterministic layout) + edge table | scripts, generated layer pages | pages exist for every 2-theme pair (55 pairs of 11 themes); contrast checked; zero JS | M | Yes (the semester can live without the visuals) |
| 2.4 | JS filter enhancement | Interactive layering | One vanilla-JS file: theme multi-select filtering over embedded JSON | assets/layers.js | with JS: filtering works; without JS: all content still present | S-M | Yes |
| 2.5 | Theme-page relation digests | Cross-theme navigation | Theme pages show the strongest outgoing relations to other themes (counts of edges) | layouts | counts match the data on spot check | S | Yes |

## Phase 3 — Interoperability

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | CSV/JSON exports | Non-specialist reuse | scripts/export.py; /downloads/ page; release assets | scripts | CSV opens in LibreOffice with correct UTF-8; JSON validates | S | No (low cost) |
| 3.2 | SKOS exports | Library/heritage reuse | scripts/export_skos.py (rdflib): ConceptScheme, Collection per theme, language-tagged labels, altLabels, broader/related + typed sub-properties (ADR-0005); Turtle + JSON-LD | scripts | loads in an RDF tool (rdflib roundtrip); IRIs = w3id URLs | M | Yes |
| 3.3 | schema.org markup | Search visibility | DefinedTerm / DefinedTermSet JSON-LD in term page heads | layouts | rich-results test passes on a term page | S | Yes |
| 3.4 | External mappings (partial) | FORRT/Wikidata alignment | Fill matches.wikidata (exactMatch) where a solid equivalent exists (about 30 terms); matches.forrt (closeMatch) where FORRT has a match | content/terms/* | mappings exported into SKOS; samples verified against Wikidata/FORRT | S-M | Yes |

## Phase 4 — Community

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Issue forms | Structured intake | .github/ISSUE_TEMPLATE/suggest-a-term.yml + report-an-error.yml (GitHub issue forms) | .github/* | submitting a form yields a complete structured issue | S | No (low cost) |
| 4.2 | Contribution docs | A contributor can act alone | CONTRIBUTING.md (incl. CC BY 4.0 acknowledgement), PULL_REQUEST_TEMPLATE.md, CODE_OF_CONDUCT.md, docs/students.md (course assignment flow) | root, docs | a student with no git experience follows the guide to a mergable PR in the pilot session | M | Yes until a cohort arrives |
| 4.3 | Review status workflow | Quality marks visible | status draft->reviewed transitions documented; "reviewed" badge on term pages; reviewer = maintainer for now, GOVERNANCE extended when others join | docs, layouts | a draft term separates visually from reviewed ones (including in exports) | S | Yes |
| 4.4 | Pilot cohort | Course activity integration | One seminar session: students pick candidate terms from candidates.yaml, draft via forms/PRs, peer-review in pairs, maintainer merges | docs/students.md | at least 3 student-authored merged terms with ORCIDs; candidate backlog reduced | course time | Yes |

## Phase 5 — Multilingual

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | i18n scaffolding | Language mechanics proven | Hugo multilingual configuration (ADR-0002); language switcher; fallback rules (missing translation -> show English + notice, no broken pages) | site config, layouts | a *.de.md file renders a DE page; a term without one renders EN with the notice | S | No (when Phase 5 starts) |
| 5.2 | Pilot batch | First German content | Translate the ~12-term pilot (OPEN-QUESTIONS Q9: publishing + policy core), reviewed by a German-language reader | content/terms/*.de.md | pilot terms display in DE; SKOS export carries de labels for them | M | Yes |
| 5.3 | Expansion | Steady state | Recurring task (one translating batch per semester, possibly as coursework) | content | DE coverage grows; untranslated share visible on the index | ongoing | - |

## Phase 6 — Long-term care

| Step | Goal | Tasks | Files | Acceptance | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 6.1 | Yearly maintenance checklist | Stays boring on purpose | 30-60 min/yr: Actions versions check, Hugo bump-or-not, link check, w3id redirect curl test, exit drill (build + throwaway deploy) | docs/maintenance.md | checklist run logged as a closed issue each year | S | No |
| 6.2 | Release hygiene | Consistent versioning | Per-release checklist (ADR-0004, ARCHITECTURE section 4): CHANGELOG generation, CITATION.cff dates, Zenodo verification, SWH save-code-now | docs | every release has: version DOI, changelog entry, SWH snapshot request | S per release | No |
| 6.3 | Handover documentation | Survival beyond the maintainer | GOVERNANCE.md: who decides, how a successor takes over (repo, w3id contact-change PR, Zenodo account note, Codeberg mirror) | GOVERNANCE.md | a named successor could execute the handover doc unaided | S | No |
| 6.4 | Succession dry run | Trust in continuity | Once: a successor (or colleague) performs a release following only the docs | - | the release completes without maintainer help | S, once | Yes, but do it before you need it |

## Ten-year failure modes (the 2036 table)

| Failure | Likelihood | Mitigation (already designed in) | Where |
| --- | --- | --- | --- |
| Static site generator abandoned | medium | single pinned tool whose only input is plain data; docs/rebuild.md written in Phase 1; content readable without any build; migration = templating exercise | ADR-0002, step 1.7 |
| GitHub policy change / Pages discontinued | low-medium | w3id redirect decouples URLs from host; the artefact deploys unchanged anywhere (UHH, Codeberg); mirror already on Codeberg; source + built site archived in Zenodo + SWH | ADR-0003, ADR-0008 |
| Link rot (external links in entries) | high | yearly link check (6.1); entries cite sources with DOIs; broken external links never break the glossary itself | 6.1 |
| Maintainer leaves | medium | GOVERNANCE + handover doc + succession dry run; every step small and documented; data files editable by a non-programmer via the web UI | 6.3, 6.4, ADR-0001 |
| JavaScript/network viz "dies" (browser APIs change) | low | no runtime JS dependency at all; layer views are static SVG + HTML tables generated at build time | ADR-0006 |
| DOI points to stale content | medium by 2036 | version DOIs freeze the exact rendered release (release assets include the built site); site footer always names the current version; term pages show date_last_changed | ADR-0004 |
| w3id.org itself degrades | low | consortium-backed; the .htaccess lives in our repo too, so redirects can be re-homed under any domain in minutes | ADR-0003 |
| Zenodo policy/availability change | low | per-release artefacts also in Software Heritage; version ZIPs frozen; concept DOI chain already referenced in the scholarly record; switching archives only changes future releases, not past ones | ADR-0004, ADR-0008 |
| Python packaging churn (validators, rdflib) | medium | three tiny, stable, pure-Python dependencies; validation runnable locally in minutes; the formats (YAML/JSON Schema/Turtle) outlive any single library | ARCHITECTURE section 3 |
| Content rot (dated facts, e.g. publisher revenue figures) | high | facts carry as-of dates + sources; CHANGELOG distinguishes substantive changes; commit history + SWH make every past state retrievable | ADR-0004, DATA-MODEL |
| Terminology shifts 2026->2036 | certain (slowly) | deprecation flow (never delete, replaced_by pointer); theme list editable as data; major version boundaries mark redefinitions | ADR-0003, semver in ADR-0004 |

## Suggested sequencing for the current semester (if approved)

```text
Week 1: 0.1-0.3 + merge this planning PR (review)
Week 2: 0.4-0.6, 1.1-1.2
Week 3: 1.3-1.4, 2.1 (relation data for the seminar chains), start the w3id PR (1.5)
Before first classroom assignment: 1.6 (v2.0.0 release) -> the site is citable
After the semester: 2.3-2.5 (visual layering), 3.x (exports), Phase 4 with next cohort
```
