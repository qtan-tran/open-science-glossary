# ADR-0008: Hosting, mirroring, and the exit drill

Status: proposed · Decides: host choice, mirror, exit strategy

## Context

Requirement: deploy unchanged to any static host; cheap to maintain for one academic; must survive a GitHub policy/page change. GitHub Pages is the pragmatic default; it stays the served host for Phase 1 (least friction with the DOI/release pipeline), but the architecture must never depend on it.

## Options considered

1. **GitHub Pages alone.** Fastest, but single point of failure; a single-platform policy change would require a scramble.
2. **University server primary.** Institutional fit, but hosting on a scholar-maintained university server usually means slower setup, and any move would render past GitHub-based URLs stale if hardcoded.
3. **GitHub Pages primary + Codeberg Pages mirror + exit drill.** Chosen.

## Decision

1. **Deploy target of record: GitHub Pages** (a built-artifact upload, no GitHub Actions-proprietary features beyond the deploy routine, no proprietary services).
2. **Mirror push job in the same release workflow**: after a successful Pages deploy, the same workflow pushes the built site to the Codeberg Pages repository (an equivalent plain static host, already in the Codeberg mirror). Codeberg Pages serves on a Codeberg-pages.de; a one-line .htaccess-equivalent notes it as the second instance; on a GitHub exodus this becomes primary within minutes, because w3id already fronts everything (ADR-0003).
3. **Exit drill (once a year, in the maintenance checklist):** build the site locally from a clean checkout of the last release tag; deploy it to a throwaway directory on any available static host (or just verify the Codeberg mirror is live and current); confirm the w3id redirect points at it and Pages could be swapped out within 15 minutes.
4. **No proprietary host features**: no GitHub-specific components (no Jekyll frontmatter hacks, no Actions-needing-pages-gates beyond a standard checkout/upload), so the output directory deploys unchanged anywhere (UHH web space included).
5. **Software Heritage archival on each release** (save code now request, plus Zenodo's own archiving); Zenodo release snapshots already include the built site, so the DOI always resolves to content even if both hosts vanished.

## Consequences

- Cost: one extra workflow job; zero additional maintenance beyond noting when the mirror pushes fail.
- Ten-year robustness: platform risk is limited to a short redirect swap; the drill makes the exit a practiced move rather than an expedition.
- Governance note: transfer of the GitHub repository alone would not carry the Codeberg mirror token; successor onboarding includes credentials/token transfer, handled in handover docs per GOVERNANCE (Phase 6).
