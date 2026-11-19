# ADR-0004: Versioning and DOI strategy

Status: proposed · Decides: semver policy, new vs. continued Zenodo record, per-term citability

## Context

The glossary must be citable as a whole, per release, and ideally per term. Zenodo's GitHub integration mints a new version DOI and one concept DOI per GitHub release; per their documentation, a repository cannot be attached to an existing concept DOI: versions map to releases (tags) of one connected repository (see Zenodo's GitHub repository integration guide). The v1.0.0 Word/PDF glossary already exists as Zenodo record 10.5281/zenodo.23449750. Making the website v1.1 of that record is not possible mechanically; pretending continuity in numbering would misrepresent what changed (a platform shift, not a patch).

## Options considered

1. **New Zenodo record starting at v2.0.0.** Semver's major bump honestly signals "new artifact generation"; cross-link both records via related identifiers ("isNewVersionOf" 10.5281/zenodo.23449750 on the new record; edit the old record to "isPreviousVersionOf"); two concept DOIs, each with an honest citation trail. Recommended.
2. **Manually upload old file + new site as one record's versions.** Abandons the GitHub integration (the source of the discipline: tagging releases); version DOI belongs to snapshots, not only releases; more manual than automatic.
3. **Deprecate-and-divert: v2.0.0 site release, old record retains v1.x citations only.** Same as 1 without related identifiers, lost continuity: rejected.

## Decision

1. **New Zenodo record** created automatically by the GitHub integration on the first tagged release, **tagged v2.0.0** (major bump marks the platform change; minor = new terms, patch = corrections).
2. **Cross-link** the two records via related identifiers, in both directions (new: cites as previous; old: add relatedIdentifier to the new version DOI once first release exists).
3. **No per-term DOIs**: each term cites its **permanent URL (w3id per ADR-0003) plus the current release version DOI** (e.g. "Tran, Q.-T. (2026). APC. In Open Science Glossary (v2.0.0). Zenodo. https://doi.org/10.5281/zenodo.XXXXX + https://w3id.org/os-glossary/term/apc"). Term identity = the permanent URL; the release DOI anchors the exact version cited. Per-term DOIs would multiply maintenance cost against a system designed for per-term stability already (slugs never reused, deprecations remain resolvable).
4. **Version freeze discipline**: release assets include the rendered site + data exports, so each version DOI resolves to a frozen copy of exactly what was released.
5. CITATION.cff in the repo root; .zenodo.json overrides if needed (creators with ORCID, license CC BY 4.0, keywords).

## Consequences

- Git history and release tags become the canonical machine-readable version chronicle; CHANGELOG.md is generated per release into the release body.
- Zenodo sandbox is used first (test with a sandbox copy of the repo) per Zenodo guidance, to avoid live mis-tagging.
- CHANGELOG entries are hand-curated before tagging, machine-generated content compiled into the release artifacts.
- Minor caveat: readers citing "the glossary" should cite the concept DOI of the NEW record; documentation (README badge, CONCEPT) will say this explicitly.
- Old record stays untouched but gains a forward pointer: nothing about v1.0.0 citations breaks.
