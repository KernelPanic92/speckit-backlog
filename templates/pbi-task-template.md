---
# id: the next free project-wide id from the validator (e.g. TASK-001); it never changes. Tool ids are added in `external` by /speckit.sync
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: TASK
# relations with other PBIs, declared only from this side:
# - PARENT: the user story this task serves (or the Epic of the Macro-Activity, for Walking Skeleton items)
# - BLOCKED_BY: the tasks that must be completed first (this replaces a free-text "Dependencies" field)
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
# optional: diagrams, technical specifications or logs useful for the work. Only links really supplied by the user
media:
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
---

## Outcome

[A clear, concise description of what has to be done technically. E.g.: "Create the login API endpoint" or "Implement the navbar CSS layout"]

<!-- optional, only for test tasks derived from Gherkin scenarios: the scenarios this task turns into automated acceptance tests -->
**Covers:** {{US-001/AC-1}}, {{US-001/AC-2}}

## Files

<!-- Exact paths this task creates or modifies, consistent with the plan's Project Structure -->
- `{{path/to/file}}`

## Actions to complete
- [ ] Sub-activity 1
- [ ] Sub-activity 2

<!-- optional section, include it only when filled in -->
## Out of Scope

<!-- Nearby technical work this task does not touch (refactoring, optimizations, adjacent parts). One bullet per item, with where it goes: the PBI that covers it (`type [id] title`) or "not planned". List only what a reader could reasonably assume is included, not everything this PBI does not do -->
- {{what is not included}}: {{where it goes}}

<!-- optional section, include it only when filled in -->
## Additional Notes

<!-- Bullet list of details that emerged during refinement, technical constraints or business logic. Write every link as [topic in clear words](address that reaches the spot: section anchor, page, Figma frame), never a bare URL, an abbreviation or a section number without its title -->

## Definition of Done (DoD)
<!-- Start from the "Task Completion Criteria" of tasks.md; keep only the items that apply and add task-specific ones -->
- [ ] The code compiles without errors / does not break the build
- [ ] Unit tests written and passing
- [ ] Technical documentation updated (if needed)
- [ ] Code review passed
