# ADR-0001: Content is data, not code

Status: proposed · Decides: one plain-text file per term

## Context

The glossary must be extendable by a non-programmer (teacher, student, successor maintainer), editable through the GitHub web interface, useful without the website, and validated automatically. The v1.0.0 artifact is a Word/PDF document whose content is currently locked into one binary file and one ad-hoc build chain.

## Options considered

1. **Markdown + YAML front matter, one file per term.** Human-readable; GitHub renders it; any SSG or script can read it; diffs are reviewable per term.
2. **Single YAML/JSON database file.** Machine-friendly, but a 60+ term file is unwieldy in review and merge-conflict prone.
3. **Keep the Word document as source of truth and convert at build.** Keeps the author's writing tool, but converting .docx in CI is fragile, non-reviewable, and the data stays unusable without the site.

## Decision

One file per term: Markdown with YAML front matter (content/terms/<slug>.md). The definition and prose live in the body; structured metadata (themes, relations, sources, contributors, dates, status) live in front matter. Themes, relation types, and languages are controlled vocabularies in their own small data files (data/themes.yaml, data/relationship-types.yaml, data/languages.yaml). A JSON Schema validates front matter in CI; a reference check fails the build on unknown slugs or themes.

## Consequences

- Adding a term, theme, relation type, or language touches only data files.
- Anyone can clone the repo and read or reuse the glossary without the website.
- The .docx/PDF remain release *artifacts* (generated from the data in Phase 1), not sources.
- Cost: a one-time migration (ROADMAP 0.4) with a verification step that nothing was lost.
