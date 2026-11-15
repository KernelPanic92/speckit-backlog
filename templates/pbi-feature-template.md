---
# id: the next free project-wide id from scripts/backlog.py next-id FEATURE (e.g. FEATURE-001); it never changes
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: FEATURE
# optional: priority rank among siblings (10, 20, 30...; lower = higher priority)
rank: {{rank}}
# optional, relations with other PBIs, declared only from this side
# BLOCKED_BY: the referenced PBI blocks this one | PARENT: the referenced PBI is the parent, at most one | RELATED: link without constraints
relations:
    "{{related id}}":
        title: "{{PBI title}}"
        type: US|FEATURE|TASK|BUG|EPIC|SPIKE|MAP
        relationType: BLOCKED_BY|PARENT|RELATED
        reason: "{{reason for the relation}}"
# optional: attachments useful across the Feature's stories. Only links really supplied by the user
media:
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
---

As a {{Persona}}, I want {{capability one level above user stories, without "and"}}, so that {{Value}}.

## Outcome

{{Measurable benefit expected for the end user or the business}}

## Constraints

<!-- Cross-story constraints for this Feature that are not Gherkin scenarios and not project-wide constitution rules. Give each constraint its source as a readable link. -->
- {{constraint}}: [{{source in clear words}}]({{link to the exact spot}})

## Out of Scope

<!-- Nearby capabilities a reader could reasonably assume are included. State where each one goes, e.g. the next Feature in the same Epic's lane, or that it is not planned. -->
- {{what is not included}}: {{where it goes, e.g. FEATURE [id] title in lane "Outcome", or not planned}}

<!-- Optional section; include it only when filled in. -->
## Assumptions

- {{assumption}}
