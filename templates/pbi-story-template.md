---
# id: the next free project-wide id from the validator (e.g. US-001); it never changes. Tool ids are added in `external` by a tracker extension
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: US
# optional, relations with other PBIs, declared only from this side (e.g. the parent epic as PARENT)
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
# optional: Figma mockups, screenshots or other attachments useful for development. Only links really supplied by the user
media:
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
---

As a {{Persona}}, I want {{Action/Goal}}, so that {{Value}}.

## Outcome

{{outcomeDescription}}

## Acceptance Criteria

### AC-1: {{acceptance.title}}

**Given** {{context or initial state}}
**When** {{action performed}}
**Then** {{observable or measurable result}}

## Out of Scope

<!-- Nearby capabilities, cases or variants that are not part of this story: the scope is fixed by the "I want" clause (the OUT part of the Micro-Scope "Technical Boundaries"). One bullet per item, with where it goes: the PBI that covers it (`type [id] title`) or "not planned". List only what a reader could reasonably assume is included, not everything this PBI does not do -->
- {{what is not included}}: {{where it goes}}

<!-- optional section, include it only when filled in -->
## Additional Notes

<!-- Bullet list of details that emerged during backlog refinement, links to Figma mockups, technical constraints or business logic. Write every link as [topic in clear words](address that reaches the spot: section anchor, page, Figma frame), never a bare URL, an abbreviation or a section number without its title -->

<!-- optional section, include it only when filled in -->
## Assumptions

- {{assumption}}

<!-- optional section, include it only when filled in -->
## Risks

- {{risk}}

## INVEST & DoR (Definition of Ready) Check
- [ ] **I**ndependent - [explain why it has no blocking dependencies]
- [ ] **N**egotiable - [explain why it leaves room for technical solutions]
- [ ] **V**aluable - [explain why it brings value to the end user]
- [ ] **E**stimable - [explain why the team knows how to estimate it]
- [ ] **S**mall - [explain why it fits comfortably in a single Sprint]
- [ ] **T**estable - [explain why it has clear acceptance criteria]
