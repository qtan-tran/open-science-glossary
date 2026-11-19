# ARCHITECTURE — Open Science Glossary website

Status: draft for review · Companion: [CONCEPT.md](CONCEPT.md) · [DATA-MODEL.md](DATA-MODEL.md) · [ROADMAP.md](ROADMAP.md)

## 1. Overview

```text
            (humans: GitHub web UI / git)          (machines)
  editors ──> content/*.md + data/*.yaml ── validation (schema + refs) ──> FAIL = red CI
                        |
                        |── build (Hugo, pinned) ──> static HTML site ──> GitHub Pages
                        |                            (deployable unchanged anywhere)
                        |── exports (Python, pinned) ──> CSV / JSON / SKOS (ttl, jsonld) ──> release assets + site/downloads/
                        `── printable sheet (PDF-ish export of Quick-Reference) ──> release artifact + classroom use
  releases: tag ──> GitHub Release ──> Zenodo record (concept DOI + version DOI, automatic) ──> Software Heritage archive
  URLs: https://w3id.org/os-glossary/...  ──302──> current host (GitHub Pages today)
```

Everything upstream of the build is plain text; everything downstream is generated. The data is usable without the site (ADR-0001); the site is deployable without GitHub (ADR-0008); links are citable without the host (ADR-0003).

## 2. Repository layout (target state)

```text
.
|── content/
|   |── terms/                  # one file per term (ADR-0001)
|   |   |── apc.md               # English (default language)
|   |   |── apc.de.md            # optional German translation (same id inside)
|   |   `── ...
|   `── about.md                # site pages (about, methodology), also plain MD
|── data/
|   |── themes.yaml             # controlled vocabulary of themes (11)
|   |── relationship-types.yaml # closed relation list (8) with SKOS mappings
|   |── languages.yaml          # en, de (+future)
|   `── candidates.yaml         # dangling references / stub plan (ROADMAP, OPEN-QUESTIONS Q5)
|── schemas/
|   |── term.schema.json        # JSON Schema for term front matter
|   `── vocabulary.schema.json  # schemas for the data/*.yaml files
|── layouts/                   # Hugo templates (MIT-licensed code)
|── assets/                    # CSS + the one optional vanilla-JS file (ADR-0006)
|── scripts/
|   |── validate.py             # schema + cross-reference + dangling-ref checks
|   |── export.py              # CSV / JSON
|   |── export_skos.py          # Turtle + JSON-LD via rdflib (pinned in requirements.txt)
|   |── build_layers.py         # static SVG diagrams for theme pairs (ADR-0006)
|   `── changelog.py            # generated CHANGELOG.md per release
|── .github/
|   |── workflows/              # validate.yml, deploy.yml, release.yml
|   |── ISSUE_TEMPLATE/        # issue forms: suggest-a-term, report-an-error
|   `── PULL_REQUEST_TEMPLATE.md, dependabot.yml
|── legacy/                    # frozen v1.0.0 sources (PDF/DOCX/old tooling); never edited
|── docs/                      # this planning set + adr/ + rebuild.md (created Phase 1)
|── CITATION.cff, LICENSE-CONTENT, LICENSE-CODE, .zenodo.json
|── CONTRIBUTING.md, CODE_OF_CONDUCT.md, GOVERNANCE.md, CHANGELOG.md
`── README.md
```

## 3. Technology choices and what each costs

| Component | Choice | Pinned via | Yearly maintenance cost | If abandoned |
| --- | --- | --- | --- | --- |
| Site generator | Hugo | exact version in two lines of deploy.yml | one version bump at most; release notes read | binary still works; migration = re-templating plain data (docs/rebuild.md); ADR-0002 |
| Validation | Python 3 stdlib + jsonschema + PyYAML | requirements.txt (exact versions) | near zero; stable libs | any equivalent validator; checks are simple |
| RDF export | Python + rdflib | requirements.txt | one bump; stable since the 2000s | Turtle/JSON-LD formats are stable standards; serializer swappable |
| CI/CD | GitHub Actions (validate, deploy, release) | workflow files | Actions evolve; checked yearly | same scripts run locally in minutes; documented |
| JS | none, except optional 1 vanilla file | no dependency at all | none | nothing to die client-side |
| Graph rendering | build-time SVG (script) | scripts/build_layers.py | small, our own, tested | tables remain canonical (ADR-0006) |
| Hosting | GitHub Pages + Codeberg mirror | deploy.yml | zero | artefact deploys anywhere; w3id redirect repoints |

Total: **one site generator + three small Python libraries**. That is the entire dependency surface. No lockfiles beyond requirements.txt (no Node runtime at all on the server side).

## 4. Build, deploy, and release pipeline

| Workflow | Trigger | Steps | Success gate |
| --- | --- | --- | --- |
| validate.yml | every push/PR to any branch | parse term files; schema-validate front matter; check every relation/see-also target and theme id exists; check candidates.yaml holds otherwise-dangling refs; basic link-lint (no dead internal URLs) | red/green on PR; required check |
| deploy.yml | push to main | run Hugo build + exports + SVG; upload artefact; deploy Pages; push mirror to Codeberg | site live at version of main |
| release.yml | tag v* | build; generate CHANGELOG.md from term dates + git history; create GitHub Release with assets (built-site.zip, glossary.csv, glossary.json, os-glossary.ttl, os-glossary.jsonld, quick-reference PDF export); Codeberg mirror tag | GitHub Release page complete |

Manual per release (the only manual steps in the whole system): run the release checklist (docs/rebuild.md, Phase 6): fill date-released + doi in CITATION.cff, publish the GitHub Release (via UI one click or gh release CLI), confirm Zenodo minted the next version DOI, then submit the tag to Software Heritage save-code-now. Rationale for the automation boundary: the Zenodo release integration keys on GitHub Release creation (verified: [Zenodo docs](https://help.zenodo.org/docs/github/)), and DOI-after-release ordering is handled by the CITATION.cff convention.

## 5. URL design and identifiers

Site URLs (stable shape, system-independent):

```text
/                     index: A–Z + themes
/term/apc/            term page
/theme/equity/        theme page with all terms + relations internal to that theme
/layers/equity+publishing/   prebuilt layer view (SVG + tables)
/downloads/           SKOS/JSON/CSV exports
/changes/             CHANGELOG rendering
```

Permanent URL layer (ADR-0003), one .htaccess under ids/os-glossary/ in the [perma-id/w3id.org repo](https://github.com/perma-id/w3id.org) (their guide: [docs.w3id.org/guides/create-an-id](https://docs.w3id.org/guides/create-an-id)):

```apache
# https://w3id.org/os-glossary/ -> current host (GitHub Pages today)
Options +FollowSymLinks
RewriteEngine on
RewriteRule ^(.*)$ https://qtan-tran.github.io/open-science-glossary/%%1 [R=302,L]

## Contact
# Maintainer: Quoc-Tan Tran, github.com/qtan-tran, ORCID 0000-0003-3533-5858
```

Citation payload every term page carries (auto-generated from release metadata):

```bibtex
@misc{osg_apc_2_0_0,
  author = {Tran, Quoc-Tan},
  title  = {{APC (Article Processing Charge)}},
  howpublished = {In \\emph{Open Science Glossary} (v2.0.0)},
  year   = {2027},
  doi    = {10.5281/zenodo.XXXXXXX},       <- version DOI, minted automatically after release
  url    = {https://w3id.org/os-glossary/term/apc}
}
```

plus an APA string, plus "how to cite the whole glossary" (concept DOI) on every page footer.

## 6. Persistence and citation strategy (summary; details in ADRs)

1. **Term slugs** never reused; deprecations keep pages and redirect data (ADR-0003).
2. **w3id URLs** are the citable canonical everywhere: page footers, exports, schema.org, SKOS IRIs, PDF export footer. Host URLs never appear in printed material.
3. **Zenodo chain** (ADR-0004): concept DOI = "the glossary"; version DOIs per release; the v1.0.0 Lesson record is related-linked in both directions. Release assets include the built artefacts so the *rendered* site version is archival too.
4. **Software Heritage** archives git history per release (ADR-0008), giving SWHIDs for any future "source of this exact page in 2029" question.
5. **CHANGELOG.md** (generated) documents per-release term-level changes; terms carry date_created / date_last_changed (see DATA-MODEL).
6. **Old versions viewable**: every Zenodo version DOI freezes the release ZIP (including the built HTML in assets), satisfying "old versions stay viewable" even without hosting old branches.

## 7. Accessibility implementation notes (WCAG 2.2 AA)

- Templates use semantic HTML (headings hierarchy, nav/main/footer, skip link); no ARIA soup.
- Layer views: SVG gets role="img" + a text alternative listing edges; the relationships table below is the canonical accessible equivalent (ADR-0006).
- Contrast, focus visibility, touch target size checked via CI axe-core on built HTML (single dev dependency) + manual checklist per release.
- Plain-language style enforced editorially (definitions under ~120 words, one misconception max, sources listed).
- prefers-reduced-motion respected; there is no motion by default.

## 8. Security, review, and admin settings (Phase 0/1 checklist items)

- Branch protection on main: PR-only, required validate check, CODEOWNERS = maintainer.
- No secrets used anywhere; deploy uses the built-in GITHUB_TOKEN.
- Dependabot watches the two pinned requirements files (nothing to watch on the front end).
- Issue forms (suggest/report, governance files) + PR template with a content checklist (licence CC BY 4.0 ack, sources present, misconception flagged).
