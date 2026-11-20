# Release checklist: v2.0.0 as a new version of the existing Zenodo record

Per docs/DECISIONS.md D-3 (one concept DOI for all versions, from the Word
edition onward; the GitHub-Zenodo integration is deliberately NOT used) and
D-11 (correct the "55 terms" wording at release time). Do not tag or upload
until the first-wave drafts are reviewed and Pages is live.

## Preconditions

- [ ] First-wave drafts reviewed; their status flipped from `draft` to `reviewed`.
- [ ] GitHub Pages live under Source: GitHub Actions (the workflow deploy.yml
      only works with that source; see issue #8).
- [ ] All CI gates green on main.
- [ ] `params.version` in hugo.toml is 2.0.0; set `preRelease = false` only
      when tagging.

## Release metadata (draft for the Zenodo "new version" form / REST API)

- `title`: Open Science Glossary
- `version`: 2.0.0
- `description` (replaces the v1.0.0 text; corrects "55 terms" per D-11):

  > The Open Science Glossary explains open science terms for everyday
  > research use. This is the first machine-readable + website edition
  > (v2.0.0), successor of the Word/PDF edition v1.0.0 (2026-10-18), which
  > contained 64 full entries; the v1.0.0 description's "55 terms" referred
  > only to the Quick-Reference sheet (corrected here). v2.0.0 contains the
  > 66 migrated term entries, the D-4 splits, and twelve first-wave new
  > entries in reviewed status. Each term page carries an APA citation and
  > BibTeX entry; the whole glossary is exportable as BibTeX. Sources:
  > UNESCO Recommendation on Open Science (2021) and the publishing and
  > bibliometrics literature. License: CC BY 4.0 (content), MIT (code).

- `license`: cc-by-4.0
- `creators`: Quoc-Tan Tran (ORCID 0000-0003-3533-5858)
- `related_identifiers`:
  - `isIdenticalTo`: https://github.com/qtan-tran/open-science-glossary
    (repository, tag v2.0.0)
  - `isSupplementTo` / website: https://qtan-tran.github.io/open-science-glossary/
    (planned w3id alias: https://w3id.org/os-glossary/)
- `notes`: mention that the concept DOI stays 10.5281/zenodo.23449750

## Upload procedure (manual, per D-3)

1. Smoke test on https://sandbox.zenodo.org first (web UI or REST API) with
   the same metadata and a small archive.
2. On https://zenodo.org, open record 10.5281/zenodo.23449750 and choose
   "New version"; upload the release archive (site content export or
   repository source archive per the release decision), paste the metadata
   above, set version 2.0.0, license CC BY 4.0.
3. Publish; verify the new version DOI resolves and that the description no
   longer says "55 terms" (D-11).
4. Tag the repository `v2.0.0`; set the returned version DOI in
   CITATION.cff (replace the concept DOI in `identifiers` with a
   `preferred-citation` entry) and in hugo.toml `params.doi`; flip
   `params.preRelease` to false; update CHANGELOG.md date.
5. Redeploy the site (the citation boxes then cite the version DOI, D-6).
