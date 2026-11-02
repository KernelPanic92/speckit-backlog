---
# id: the next free project-wide id from the validator (e.g. EPIC-001); it never changes. Tool ids are added in `external` by /speckit.sync
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: EPIC
# optional, relations with other PBIs, declared only from this side (e.g. the User Story Map this Epic is a Macro-Activity of, as PARENT; PBIs that block it as BLOCKED_BY)
# BLOCKED_BY: the referenced PBI blocks this one | PARENT: the referenced PBI is the parent, at most one | RELATED: link without constraints
relations:
    "{{related id}}":
        title: "{{PBI title}}"
        type: US|TASK|BUG|EPIC|SPIKE|MAP
        relationType: BLOCKED_BY|PARENT|RELATED
        reason: "{{reason for the relation}}"
    "{{related id}}":
        title: "{{PBI title}}"
        type: US|TASK|BUG|EPIC|SPIKE|MAP
        relationType: BLOCKED_BY|PARENT|RELATED
        reason: "{{reason for the relation}}"
---

As a {{Persona}}, I want {{Action/Goal}}, so that {{Value}}.

## Outcome

{{outcomeDescription}}

## Scope Boundaries
To avoid *scope creep* (the uncontrolled growth of requirements), we set the boundaries up front:
- **In Scope (what we will do):**
  - [ ] Capability A
  - [ ] Capability B
- **Out of Scope (what we will NOT do in this Epic):**
  - [ ] Integration with system Y (a future Epic)
  - [ ] Support for legacy versions

<!-- macro-scope acceptance criteria -->
## Acceptance Criteria

### AC-1: {{acceptance.title}}

**Given** {{context or initial state}}
**When** {{action performed}}
**Then** {{observable or measurable result}}

## Additional Notes
[Legal, marketing or cross-team dependencies, links to architecture documents / Figma]

<!-- optional sections, include them only when filled in -->
## Assumptions

- {{assumption}}

## Risks

- {{risk}}
