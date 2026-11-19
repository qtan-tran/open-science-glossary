# ADR-0002: Static site generator

Status: proposed · Decides: which tool builds the HTML

## Context

The site must build in 2036 with one academic maintainer who has little time. Requirements: plain HTML/CSS output, versions pin-able, core reading works without JavaScript, no server, no database. Alternatives were evaluated against: time-to-first-site, yearly maintenance cost, risk of abandonment, and cost-of-migration if the tool dies.

## Options considered

1. **Hugo** (single compiled Go binary). Pros: no runtime dependencies, no node_modules, very fast, native support for the two hard requirements: taxonomies (themes are exactly this) and multilingual content (translation files by suffix, e.g. apc.de.md); large community; an archived binary still builds the site even if the project died. Cons: Go template language is unfamiliar to JS/Python people; single-maintainer project (though stable since 2013).
2. **Eleventy.** Pros: JavaScript, simple mental model, large community. Cons: Node ecosystem churn (v2/v3 ESM transitions already broke plugins); lockfile and node_modules oppose the "boring in 2036" goal; taxonomies and multilingual must be hand-rolled.
3. **Small build script (Python) + templates.** Pros: zero framework lock-in. Cons: we would own every feature (taxonomies, pagination, i18n) forever; the code becomes the legacy to maintain.
4. **No build; commit HTML.** Rejected: duplicates content storage and Makes edits error-prone.

## Decision

**Hugo**, pinned in the workflow (one version variable), with docs/rebuild.md covering: the exact pinned version, how to obtain/build the same Hugo binary, and the guarantee that migration is a templating exercise because all content is plain data (ADR-0001). Eleventy is revisited only if Hugo fails a Phase 1 requirement. Final confirmation pending planning review (OPEN-QUESTIONS Q2).

## Consequences

- Deployment is uploading a directory; works on GitHub Pages, Codeberg Pages, or a UHH static server unchanged.
- Taxonomies and multilingual come built in; the interactive layer view stays outside Hugo (ADR-0006).
- Maintenance cost: one tool, at most one version bump per year (yearly checklist, ROADMAP Phase 6).
