# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Status**: Draft

**Input**: [User description: "$ARGUMENTS" — or the starting PBI as type [id](../../backlog/...) title]

**Scope**: `[PBI-ID, e.g. FEATURE-001]` *(comma-separated PBI IDs of type MAP, EPIC, FEATURE, or US whose requirements this spec covers)*

## Backlog

<!--
  The block between the markers is rendered deterministically by
  `scripts/backlog.py render-spec <spec-dir>` from **Scope** and the repository-root `backlog/`.
  It includes PBIs nested under MAP / EPIC / FEATURE ancestors, ordered by delivery wave and `rank`,
  with `[P]` markers for parallelizable stories and links to `../../backlog/...`.
  MUST NOT hand-edit anything between the markers.
-->
<!-- BEGIN BACKLOG -->
<!-- END BACKLOG -->

## Key Entities *(include if feature involves data)*

<!-- Use exact Ubiquitous Language terms from [.specify/memory/product.md](../../.specify/memory/product.md#ubiquitous-language). Remove this section if no data is involved. -->

- **[Entity 1]**: [What it represents, key attributes and relationships without implementation details]

## Success Criteria *(mandatory)*

<!-- Technology-agnostic, measurable outcomes derived from the Outcome of the scoped Feature / Epic / User Stories. Cite a criterion as SC-001 "Short name". -->

### Measurable Outcomes

- **SC-001 — [Short name]**: [Measurable metric, e.g., "Shoppers complete a first purchase in under 3 minutes"]
- **SC-002 — [Short name]**: [Measurable metric, e.g., "95% of catalog searches return results in under 1 second"]

<!-- No FR-###, Edge Cases, Assumptions, or separate unanswered-question sections belong here. Scenarios, edge cases, exclusions, and functional assumptions live in the PBIs under `backlog/`. `## Clarifications` is appended here only by `/speckit.clarify` when Q&A sessions occur. -->
