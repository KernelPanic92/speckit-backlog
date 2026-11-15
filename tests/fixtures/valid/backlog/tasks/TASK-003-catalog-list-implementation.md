---
id: TASK-003
title: Implement catalog list
type: TASK
rank: 20
relations:
  US-001:
    title: Catalog list
    type: US
    relationType: PARENT
    reason: Deliver the catalog list behavior.
  TASK-002:
    title: Catalog list acceptance tests
    type: TASK
    relationType: BLOCKED_BY
    reason: Implement against the executable catalog scenarios.
---

## Outcome

Serve current catalog names and prices with loading and empty states.

## Files

- `app/catalog.py`
- `app/views/catalog.html`

## Actions to complete

- [ ] Query available products and expose catalog results.
- [ ] Render loading, populated and empty states.

## Out of Scope

- Product details: not planned.

## Definition of Done

- [ ] Catalog acceptance scenarios pass.
