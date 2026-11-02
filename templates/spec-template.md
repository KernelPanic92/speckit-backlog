<!--
  SPEC ENVELOPE (preset "backlog")

  This template is NOT a whole spec. `spec.md` is made of:
    1. the ROOT PBI of the chosen mode, from its template:
       map   -> pbi-map-template   (type: MAP)
       epic  -> pbi-epic-template  (type: EPIC)
       story -> pbi-story-template (type: US)
    2. followed by the sections below, which exist ONLY in spec.md (never in the child PBIs under backlog/).

  Remove this comment block from the generated spec.md.
  Optional sections: include them only when relevant; remove them entirely instead of writing "N/A".
-->

## Spec Context

**Mode**: [map | epic | story]

**Root PBI**: [TYPE [ID] Title]

**Product context**: `.specify/memory/product.md` (Personas, Ubiquitous Language)

**Status**: [Draft | Clarified | Ready for plan]

**Input**: User description: "$ARGUMENTS"

## Backlog Index

<!--
  ACTION REQUIRED: list every child PBI of this spec with a relative link, grouped and ordered
  as the rules require: by Release Lane and then left to right along the Backbone (map mode),
  in BLOCKED_BY / release order (epic mode). Never Epic by Epic.
  Story mode: list the Spikes (if any); the TASK PBIs are listed by tasks.md, not here.
-->

### [Release 1: Outcome title | Stories | Spikes]

- [TYPE [ID] Title](backlog/[stories|epics|spikes|tasks]/[ID]-[slug].md)

## Success Criteria

<!--
  ACTION REQUIRED: measurable, technology-agnostic outcomes for the whole spec.
  Lane-level metrics stay in the MAP's Release Lanes; these are the spec-level goals.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Customers complete a first purchase in under 3 minutes"]
- **SC-002**: [Business metric, e.g., "Searches without results drop below 5%"]

## Key Entities *(include if the spec involves data)*

<!-- Domain entities, without implementation details, named with the Ubiquitous Language terms of product.md. They feed the plan's Data Model. -->

- **[Entity 1]**: [What it represents, key attributes, relationships]

## Non-Functional Requirements *(optional)*

<!--
  Container-level constraints with exact, quantitative values (no "fast", "secure", "user-friendly").
  Following the "core value first, NFR later" splitting rule, the stories that deliver
  demanding NFRs are sliced separately: reference them here.
-->

- **Performance**: [e.g., "Search results appear in under 1 second for 95% of queries"]
- **Accessibility**: [e.g., "WCAG 2.2 AA"]
- **Scalability**: [e.g., "10,000 products, 500 concurrent shoppers"]

## External Dependencies *(optional)*

<!-- Third-party systems, other teams or other specs this spec depends on. Dependencies between PBIs are expressed with BLOCKED_BY relations, not here. -->

- [Dependency]: [What we need from it and its status]

## Security & Compliance Checklist *(optional)*

<!-- Required for every spec that handles user data. Customize from the constitution's Security Posture and product.md's Business & Legal Constraints. -->

- [ ] Data classification: [Public / Internal / Confidential / Restricted]
- [ ] Authentication and authorization model identified
- [ ] Sensitive data handling described
- [ ] GDPR Article 25 (data protection by design) reviewed
- [ ] Data retention policy defined
- [ ] Right-to-erasure pathway documented
- [ ] Audit logging requirements identified

## Open Questions

<!--
  Questions that could not be answered while writing the backlog. Each one names the PBIs it affects.
  /speckit.clarify works through this list; resolved questions move to Clarifications.
-->

- [ ] Q1: [Question] — affects [TYPE [ID] Title]

## Clarifications

<!-- Written by /speckit.clarify: one "### Session YYYY-MM-DD" heading per session, then "- Q: … → A: …" bullets. -->

## References *(optional)*

- [Link to design mockups, research, related specs]
