---
title: "About"
description: "What this glossary is, how it is built, and how to contribute or reuse it."
---

## What this is

The Open Science Glossary defines key terms in open science and scholarly communication. It started as a teaching glossary in Word (v1.0.0, October 2026, published on [Zenodo](https://doi.org/10.5281/zenodo.23449750)); this site is its second edition, rebuilt as open data and an open static site (v2.0.0).

The v1.0.0 text was written by Quoc-Tan Tran in the context of university teaching in open science and cultural anthropology; the Word edition grew out of preparing a course around the FOR2026 conference (Munich, May 2026).

## How it is built

One plain-text file per term (`content/terms/`) is the single source of truth; everything on this site is generated from those files. Every change is validated in CI; a scripted check guarantees that no definition text from v1.0.0 was lost in migration, and every cross-reference must point at an existing term or the build fails (decision D-5). The site generator is a pinned version of Hugo, and [the rebuild path is documented](https://github.com/qtan-tran/open-science-glossary/blob/main/docs/rebuild.md) in case the tool is ever abandoned.

## Reuse and citation

- All content is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); site code is MIT.
- Cite the glossary by its Zenodo concept DOI, which always resolves to the current version: [10.5281/zenodo.23449750](https://doi.org/10.5281/zenodo.23449750).
- Glossary entries and definitions from NC or ND licensed sources (e.g. the FORRT glossary) are linked, never copied.
- Term URLs are permanent identifiers: `https://w3id.org/os-glossary/term/<slug>`.

## Contribute

Corrections and suggestions are welcome from anyone; see [CONTRIBUTING.md](https://github.com/qtan-tran/open-science-glossary/blob/main/CONTRIBUTING.md). The maintainer makes final calls (short governance is in CONTRIBUTING; a full GOVERNANCE.md is planned).

## Roadmap

A reviewed German pilot edition (about 12 terms) and first-wave new terms (Open Science, Open Data, OER, and others) are on the roadmap. Term pages and quick-reference sheets are generated, so new content appears everywhere at once.
