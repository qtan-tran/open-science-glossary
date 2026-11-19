# ADR-0006: Accessibility, progressive enhancement, and the layer/network view

Status: proposed · Decides: JavaScript policy, network view accessibility strategy

## Context

Layering however must not compromise: WCAG 2.2 AA for a mixed-discipline student audience; every-capability access in 2036 browser environments (hence no framework lock-in); and the maintainer's limited time. Interactive graph libraries (D3, sigma.js, Cytoscape) fail all three: they are JavaScript-required, visually-canonical, and abandoned-community risks.

## Options considered

1. **Interactive JS graph library (D3 force layout, Cytoscape).** Rejected: JS-required, heavy library to freeze for 10 years, and screen-inaccessible by default.
2. **Build-time SVG per theme-pair; no runtime JS at all.** Deterministic layout computed at build time, static SVG; an adjacent HTML table of the same edges guarantees non-visual access. Chosen.
3. **JS graph as progressive enhancement over 2's HTML (the curated subset in JS):** elected against; keeping the whole experience no-JS is a tighter guarantee against the 2036 problem, and precomputed subset lists are what the pedagogy (session chains) actually needs.

## Decision

1. **Core reading must function with JS disabled** (term pages, search via native in-page text search on the all-terms page, cross-links). No runtime JS required for any content.
2. **Layer view = build-time artifacts:** for each theme pair meeting size thresholds, build_layers.py computes a deterministic vertical grid layout (no physics simulation), writes a static SVG + emits the same edges as a relationships table in HTML. The table is the canonical accessibility equivalent; the SVG is the visual convenience.
3. **One optional vanilla-JS enhancement** (a few lines, no dependency): theme multi-select that filters the pre-rendered list/output; feature-detected, fails silently in old browsers.
4. No framework, no bundler, no runtime DOM library at all. CSS is one small static stylesheet, system fonts only (also avoids licensing issues with bundled/embedded fonts).
5. **axe-core checks in CI** at the built-site level (checking a sample of pages, incl. one layer page, for contrast, headings, labels) so the WCAG 2.2 AA target is regression-tested rather than aspirational.

## Consequences

- A screen-reader user gets the same pedagogical content via the table; a sighted user gets the visual.
- 2036 robustness: no JS API, no browser breakage vector; SVG is as durable as HTML.
- Cost: SVG layout code is one small Python script with a deterministic algorithm.
