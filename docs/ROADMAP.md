# ROADMAP — Open Science Glossary website

Status: approved 2026-11-19 (maintainer review; decisions in [DECISIONS.md](DECISIONS.md)) · Effort units: **S** = one focused working session (up to 2h), **M** = half a day.
**[TB]** = teaching blocker: must be finished before the glossary is first assigned to students in the running Winter Semester.

Only phases 0 and 1 are teaching blockers, plus 2.1 (relation *data*, because the equity-session chain is the site's pedagogical core). Everything else can slip a semester without harm.

## Phase 0 — Foundations

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 [TB] | Seed repo | Put the frozen sources in version control | legacy/ (v1.0.0 source DOCX + PDF export only, no old tooling, D-1); README.md, LICENSE-CONTENT (CC BY 4.0), LICENSE-CODE (MIT), short governance section in CONTRIBUTING.md (D-10) | legacy/ committed and never edited again; licences visible on the repo landing page | S | No |
| 0.2 | Scaffold data model | Controlled vocabularies live as data files | data/themes.yaml (11 themes), data/relationship-types.yaml (8 types), data/languages.yaml (docs/BACKLOG-TERMS.md replaces candidates.yaml: no stubs; dangling refs fail the build, D-5) | files parse; ids match DATA-MODEL | S | No |
| 0.3 | Schema + validator | Validation exists before content migrates | schemas/term.schema.json, schemas/vocabulary.schema.json, scripts/validate.py, requirements.txt (pinned) | validate.py rejects a deliberately broken sample term and accepts a valid one (smoke test) | S-M | No |
| 0.4 [TB] | Migration | 1:1 extraction of v1.0.0 into term files (script or semi-manual conversion of the DOCX), front matter minimum: id, title, themes, dates, status, sources, contributors; body conventions preserved (definition / details / warning / see-also as related) | content/terms/*.md, scripts (migration tool kept in legacy/ workflow notes) | all 64 DOCX headings map to a term file or altLabel (D-11); a scripted word-for-word comparison of DOCX vs. generated output shows no definition text lost; every see-also target resolves (dangling ones removed to docs/BACKLOG-TERMS.md, otherwise the build fails); the Quick-Reference sheet is generated from the term files | M | No |
| 0.5 [TB] | Theme assignment | Apply the theme table drafted in DATA-MODEL section 7 | content/terms/* | validate passes with themes required | S (with 0.4) | No |
| 0.6 [TB] | CI hygiene | The repo enforces its own rules | .github/workflows/validate.yml, CITATION.cff (no .zenodo.json and no GitHub integration: publishing stays in record 10.5281/zenodo.23449750, D-3), branch protection, CODEOWNERS | a red PR is blocked and a green one merges; the CFF validates | S | No |

## Phase 1 — Minimum citable site

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 [TB] | Site skeleton | Hugo (pinned) builds terms into pages: term page (definition, details, warning, relationships), A-Z index, theme pages; system font stack, semantic HTML, skip link | layouts/*, assets/*, site config | hugo --minify builds with zero warnings; all term pages reachable; one small CSS file only | M | No |
| 1.2 [TB] | No-JS reading core | One "all terms" page (headings + one-line definitions) + per-theme pages; browser in-page search is the JS-off search | layouts | JS-disabled walkthrough: any term findable, every cross-link works | S | No |
| 1.3 [TB] | Term citations | APA + BibTeX partial per term (release-versioned placeholder until the first DOI mints); footer with the whole-glossary citation | layouts/partials | copied BibTeX parses (generated bib compiles in a CI smoke test) | S | No |
| 1.4 [TB] | Deploy | Build, deploy to GitHub Pages; Codeberg mirror push job (ADR-0008) | .github/workflows/deploy.yml | live URL serves the built site; local build vs served page diff is clean | S | No |
| 1.5 | Permanent URLs | Namespace os-glossary confirmed unclaimed (live check 2026-11-19, D-7); fork perma-id/w3id.org; add ids/os-glossary/.htaccess per ADR-0003 (rules tested); open PR upstream (their guide: docs.w3id.org/guides/create-an-id) | upstream repo only | curl -sIL https://w3id.org/os-glossary/term/apc returns 302 then 200 | S (plus upstream merge wait) | Can slip past semester start: cite the GitHub Pages URL until merged |
| 1.6 [TB] | First release v2.0.0 | Tag v2.0.0; publish as a new version of Zenodo record 10.5281/zenodo.23449750 (web UI or REST API, smoke-tested on sandbox.zenodo.org first, D-3); verify the new version DOI under the existing concept DOI; correct the record description wording ("55 terms", D-11); README badges | tag, CHANGELOG.md (generated) | Zenodo shows correct metadata and wording; the concept DOI 10.5281/zenodo.23449750 resolves to the latest version (v2.0.0) | S | No |
| 1.7 | Rebuild doc | docs/rebuild.md: pinned tools, local build steps, migration story if Hugo dies | docs/rebuild.md | a colleague with no context can follow it | S | Yes (strongly recommended) |

## Phase 2 — Relationships and layering

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 [TB for content] | Relation data | Curate typed relations (start with the three CONCEPT worked examples; 40-60 edges total), one-line reasons, real entries only; include the two decided split edges (D-4): Replication --contrasts-with--> Reproducibility, Science Sleuths --is-part-of--> Post-publication peer review | content/terms/* | validate passes; the three CONCEPT chains render fully | M | The chains needed for the semester sessions: no |
| 2.2 | Relationships table UI | Term pages render the Relationships table (relation, direction, partner, reason) | layouts/partials | screen-reader spot test passes; all edges visible bidirectionally | S | No |
| 2.3 | Layer pages (static) | scripts/build_layers.py produces per-theme-pair pages: filtered term list + SVG (deterministic layout) + edge table | scripts/build_layers.py, generated layer pages | pages exist for every 2-theme pair (55 pairs); contrast checked; zero JS | M | Yes (the semester can live without the visuals) |
| 2.4 | JS filter enhancement | One vanilla-JS file: theme multi-select filtering over embedded JSON | assets/layers.js | with JS: filtering works; without JS: all content present | S-M | Yes |
| 2.5 | Theme-page relation digests | Theme pages show outgoing edge counts per other theme | layouts | spot-checked counts match the data | S | Yes |
| 2.6 | First-wave new terms | Write full entries for the 11-term first wave (D-5, docs/BACKLOG-TERMS.md): Open Science, Open Data, Open Educational Resources, DOAJ, Publication Bias, Indigenous Data Sovereignty, Serials Crisis/Big Deal, Bibliometrics, Altmetrics, PKP, Retraction Watch/PubPeer; apply the three alias decisions | content/terms/* | validate passes; first-wave terms ship in v2.0.0 if finished in time, else v2.1.0 | M | Yes (target v2.1.0) |

## Phase 3 — Interoperability

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | CSV/JSON exports | scripts/export.py; /downloads/ page; release assets | scripts/export.py | CSV opens in LibreOffice with correct UTF-8; JSON validates | S | No (low cost) |
| 3.2 | SKOS exports | scripts/export_skos.py (rdflib): ConceptScheme, Collection per theme, language-tagged labels, altLabels, broader/related + typed sub-properties (ADR-0005); Turtle + JSON-LD | scripts/export_skos.py | loads in an RDF tool (rdflib roundtrip); IRIs = w3id URLs | M | Yes |
| 3.3 | schema.org markup | DefinedTerm / DefinedTermSet JSON-LD in term page heads | layouts | rich-results test passes on a term page | S | Yes |
| 3.4 | External mappings (partial) | Fill matches.wikidata (exactMatch) where a solid equivalent exists (about 30 terms); matches.forrt (closeMatch) where FORRT has a match | content/terms/* | mappings exported into SKOS; samples verified against Wikidata/FORRT | S-M | Yes |

## Phase 4 — Community

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Issue forms | GitHub issue forms: suggest-a-term, report-an-error | .github/ISSUE_TEMPLATE/* | submitting a form yields a complete structured issue | S | No (low cost) |
| 4.2 | Contribution docs | CONTRIBUTING.md (incl. CC BY 4.0 ack), PULL_REQUEST_TEMPLATE.md, CODE_OF_CONDUCT.md, docs/students.md (course assignment flow) | root, docs | a student with no git experience follows the guide to a mergable PR in the pilot session | M | Yes, until a cohort arrives |
| 4.3 | Review status workflow | status draft->reviewed transitions documented; "reviewed" badge on term pages; GOVERNANCE extended when others join | docs, layouts | a draft term separates visually from reviewed ones (including exports) | S | Yes |
| 4.4 | Pilot cohort | One seminar session: students pick docs/BACKLOG-TERMS.md terms, draft via forms/PRs, peer-review in pairs, maintainer merges | docs/students.md | at least 3 student-authored merged terms with ORCIDs; docs/BACKLOG-TERMS.md reduced | course time | Yes |

## Phase 5 — Multilingual

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | i18n scaffolding | Hugo multilingual config (ADR-0002); language switcher; fallback rules (missing translation -> English + notice, no broken pages) | site config, layouts | a *.de.md file renders a DE page; a term without one renders EN with the notice | S | No (when Phase 5 starts) |
| 5.2 | Pilot batch | Translate the 12-term pilot (D-9: APC, Diamond/Gold/Green OA, Embargo Period, Secondary Publication Right (Zweitveröffentlichungsrecht), Plan S, DORA, CoARA, Read-and-Publish (DEAL), Repository, DOI), native-speaker review required | content/terms/*.de.md | pilot terms display in DE; SKOS export carries de labels; no translation shows as reviewed without native-speaker sign-off (D-9) | M | Yes |
| 5.3 | Expansion | Recurring batches (one per semester, possibly coursework) | content/ | DE coverage grows; untranslated share visible on the index | ongoing | - |

## Phase 6 — Long-term care

| Step | Goal | Tasks | Files | Acceptance criteria | Effort | Skippable? |
| --- | --- | --- | --- | --- | --- | --- |
| 6.1 | Yearly maintenance checklist | 30-60 min/yr: Actions versions check, Hugo bump-or-not, link check, w3id redirect curl test, exit drill (build + throwaway deploy) | docs/maintenance.md | checklist run logged as a closed issue each year | S | No |
| 6.2 | Release hygiene | Per-release checklist (ADR-0004, ARCHITECTURE section 4): CHANGELOG generation, CITATION.cff dates, Zenodo verification, SWH save-code-now | docs | every release has: version DOI, changelog entry, SWH snapshot request | S per release | No |
| 6.3 | Handover documentation | Full GOVERNANCE.md: who decides, how a successor takes over (repo, w3id contact-change PR, Zenodo account note, Codeberg mirror) | GOVERNANCE.md | a named successor could execute the handover doc unaided | S | No |
| 6.4 | Succession dry run | Once: a successor (or colleague) performs a release following only the docs | - | the release completes without maintainer help | S, once | Yes, but do it before you need it |

## Ten-year failure modes (the 2036 table)

| Failure | Likelihood | Mitigation (already designed in) | Where |
| --- | --- | --- | --- |
| Static site generator abandoned | medium | single pinned tool whose only input is plain data; docs/rebuild.md written in Phase 1; content readable without any build; migration = templating exercise | ADR-0002, step 1.7 |
| GitHub policy change / Pages discontinued | low-medium | w3id redirect decouples URLs from host; the artefact deploys unchanged anywhere (UHH, Codeberg); mirror already on Codeberg; source + built site archived in Zenodo + SWH | ADR-0003, ADR-0008 |
| Link rot (external links in entries) | high | yearly link check (6.1); entries cite sources with DOIs; broken external links never break the glossary itself | 6.1 |
| Maintainer leaves | medium | GOVERNANCE + handover doc + succession dry run; every step small and documented; data files editable by a non-programmer via the web UI | 6.3, 6.4, ADR-0001 |
| JavaScript / network viz "dies" (browser APIs change) | low | no runtime JS dependency at all; layer views are static SVG + HTML tables generated at build time | ADR-0006 |
| DOI points to stale content | medium by 2036 | version DOIs freeze the exact rendered release (release assets include the built site); site footer always names the current version; term pages show date_last_changed | ADR-0004 |
| w3id.org itself degrades | low | consortium-backed and pledged; the .htaccess lives in our repo too, so redirects can be re-homed under any domain in minutes | ADR-0003 |
| Zenodo policy / availability change | low | per-release artefacts also in Software Heritage; version ZIPs frozen; the concept DOI chain is already referenced in the scholarly record; switching archives only changes future releases, not past ones | ADR-0004, ADR-0008 |
| Python packaging churn (validators, rdflib) | medium | three tiny, stable, pure-Python dependencies; validation runnable locally in minutes; the formats (YAML / JSON Schema / Turtle) outlive any single library | ARCHITECTURE section 3 |
| Content rot (dated facts, e.g. publisher revenue figures) | high | facts carry as-of dates + sources; CHANGELOG distinguishes substantive changes; commit history + SWH make every past state retrievable | ADR-0004, DATA-MODEL |
| Terminology shifts 2026->2036 | certain (slowly) | deprecation flow (never delete, replaced_by pointer); theme list editable as data; major version boundaries mark redefinitions | ADR-0003, semver in ADR-0004 |

## Suggested sequencing for the current semester (if approved)

```text
Week 1: 0.1-0.3 + merge this planning PR (review)
Week 2: 0.4-0.6, 1.1-1.2
Week 3: 1.3-1.4, 2.1 (relation data for the seminar chains), start the w3id PR (1.5)
Before first classroom assignment: 1.6 (v2.0.0 release) -> the site is citable
After the semester: 2.3-2.6 (visual layering + first wave), 3.x (exports), Phase 4 with the next cohort
```
