---
# id: the next free project-wide id from the validator (e.g. SPIKE-001); it never changes. Tool ids are added in `external` by /speckit.sync
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: SPIKE
# optional, relations with other PBIs, declared only from this side (e.g. the epic or user story it belongs to as PARENT)
# BLOCKED_BY: the referenced PBI blocks this one | PARENT: the referenced PBI is the parent, at most one | RELATED: link without constraints
relations:
    "{{related id}}":
        title: "{{PBI title}}"
        type: US|TASK|BUG|EPIC|SPIKE|MAP
        relationType: BLOCKED_BY|PARENT|RELATED
        reason: "{{reason for the relation}}"
# optional: provider documentation or existing prototypes to start the research from. Only links really supplied by the user
media:
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
---

## Outcome

[The technical or functional uncertainty to reduce, phrased as a question that can be answered. E.g.: "Does the provider support updating an existing contact without overwriting its tags?"]

## Timebox

[Maximum time spent on the research, e.g. "1 day". When the time is up the Spike closes with what has been found, even if the answer is partial.]

## Expected output

[What the Spike produces: a documented answer, a recommendation, a revised estimate of the PBI it unblocks, a throwaway prototype. It does not produce production code. In spec-kit the answer is recorded by `/speckit.plan` (Phase 0) as a decision of the feature's research, which the Exit Criteria link by its topic.]

## Out of Scope

<!-- Nearby questions this Spike does not answer and alternatives it does not explore. One bullet per item, with where it goes: the PBI that covers it (`type [id] title`) or "not planned". List only what a reader could reasonably assume is included, not everything this PBI does not do -->
- {{what is not included}}: {{where it goes}}

## Exit Criteria
<!-- When the answer is recorded, /speckit.plan ticks the first item and turns it into a link to the decision, e.g. "The question has a documented answer: [the payment provider decision](../../research.md#payment-provider)" -->
- [ ] The question has a documented answer in the feature's research
- [ ] The blocked PBIs can be estimated or revised

<!-- optional section, include it only when filled in -->
## Additional Notes

<!-- Bullet list of links, known constraints or sources to consult. Write every link as [topic in clear words](address that reaches the spot: section anchor, page, Figma frame), never a bare URL, an abbreviation or a section number without its title -->
