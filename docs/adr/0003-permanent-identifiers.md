# ADR-0003: Permanent identifiers, slugs, and the w3id.org layer

Status: proposed · Decides: how term URLs survive renames and platform moves

## Context

Every term must be citable with a stable, never-reused identifier that survives label renames and a future move away from GitHub. Raw *.github.io URLs fail on both counts.

## Options considered

1. **Own domain (e.g. os-glossary.org).** Full control, but yearly renewal forever by one academic; a lapsed domain is the classic ten-year failure. Reject for now; possible later without changing anything else (the redirect layer just repoints).
2. **GitHub Pages URLs only.** Zero cost, but platform-bound; a move breaks every citation ever made.
3. **w3id.org redirect namespace** (e.g. https://w3id.org/os-glossary/term/apc). Free, HTTPS-only redirect service run by the W3C Permanent Identifier Community Group (not a W3C standard); identifiers are a directory under ids/ in the public perma-id/w3id.org repository containing an .htaccess with Apache rewrite rules plus maintainer contact incl. a GitHub username; created by pull request or by email to the maintainers' list, per the official create-an-identifier guide (docs.w3id.org/guides/create-an-id).

## Decision

- **Term identity = slug** (e.g. apc): lowercase, hyphen-separated, never reused or recycled. Renames change the human label only. A deprecated term stays resolvable with status: deprecated and replaced_by; the page visibly points to its replacement and the old slug is never re-issued.
- **Permanent URL layer at w3id.org**: one namespace ids/os-glossary/.htaccess redirecting (302) https://w3id.org/os-glossary/... to the current host. Everything we print, cite, or embed in exports uses w3id URLs, never the host URL. If the site later moves (UHH server, Codeberg), one PR to perma-id/w3id.org preserves all literature citations.
- Site URLs mirror the same shape (/term/apc/, /theme/equity/), so redirects keep paths intact.

## Consequences

- Citation text, SKOS concept IRIs, and schema.org URLs all anchor on w3id URLs (ADR-0005).
- Counterparty risk (w3id itself) is documented in the ten-year failure table (ROADMAP); mitigation: redirects are trivial to replicate elsewhere because the .htaccess also lives in our repo, and Zenodo + Software Heritage archives preserve the content.
- Administrative cost: one upstream PR at setup and one per hosting move; maintainer contact details must be kept current (their governance asks for visible outgoing/incoming maintainers on transfer).
