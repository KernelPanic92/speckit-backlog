---
id: TASK-002
title: Catalog list query
type: TASK
relations:
    "US-001":
        title: "Catalog list"
        type: US
        relationType: PARENT
        reason: "Story served by this task"
    "TASK-001":
        title: "Static product list"
        type: TASK
        relationType: BLOCKED_BY
        reason: "Builds on the skeleton list"
---

## Outcome

Query the products for sale and render them.

## Files

- `src/catalog/list.ts`

## Actions to complete
- [ ] Query products for sale

## Out of Scope

- Product detail — not planned

## Definition of Done (DoD)
- [ ] Unit tests written and passing
