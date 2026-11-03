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
  References follow the "Readable references" rules of the backlog preset: a PBI as `type [id] title`,
  a scenario as `US-001/AC-1 "title"`, another document as a relative link whose text names the topic
  and whose address ends with the heading anchor; never a bare id, a bare path or a section number.
-->

## Spec Context

**Mode**: [map | epic | story]

**Root PBI**: [TYPE [ID] Title]

**Product context**: [Personas](../../.specify/memory/product.md#personas) and [Ubiquitous Language](../../.specify/memory/product.md#ubiquitous-language) of the product

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

<!-- Other documents cite a criterion by id and short name, e.g. SC-001 "First purchase in under 3 minutes". -->

- **SC-001 [Short name]**: [Measurable metric, e.g., "Customers complete a first purchase in under 3 minutes"]
- **SC-002 [Short name]**: [Business metric, e.g., "Searches without results drop below 5%"]

## Key Entities *(include if the spec involves data)*

<!-- Domain entities, without implementation details, named with the Ubiquitous Language terms of product.md. They feed the plan's Data Model. -->

- **[Entity 1]**: [What it represents, key attributes, relationships]

## Non-Functional Requirements *(optional)*

<!--
  Container-level constraints with exact, quantitative values (no "fast", "secure", "user-friendly").
  Following the "core value first, NFR later" splitting rule, the stories that deliver
  demanding NFRs are sliced separately: reference them here as `type [id] title`.
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
  Questions that could not be answered while writing the backlog. Each one is a full question that
  makes sense on its own and names the PBIs it affects. No numbering such as "Q1": a question is
  cited by its topic. /speckit.clarify works through this list; resolved questions move to Clarifications.
-->

- [ ] [Question?] — affects [TYPE [ID] Title](backlog/[stories|epics|spikes]/[ID]-[slug].md)

## Clarifications

<!-- Written by /speckit.clarify: one "### Session YYYY-MM-DD" heading per session, then "- Q: … → A: …" bullets. -->

## References *(optional)*

<!-- One bullet per source, as a link whose text says what it is: [Checkout mockups in Figma](https://…), [the payment provider decision](research.md#payment-provider). Never a bare URL or path. -->

- [[What the source is, in words]](address that reaches the spot)
