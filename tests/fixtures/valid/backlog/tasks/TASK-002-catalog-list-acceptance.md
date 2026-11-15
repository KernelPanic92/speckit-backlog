---
id: TASK-002
title: Catalog list acceptance tests
type: TASK
rank: 10
relations:
  US-001:
    title: Catalog list
    type: US
    relationType: PARENT
    reason: Automate the catalog list acceptance scenarios.
---

## Outcome

Executable catalog scenarios cover available products and an empty catalog.

**Covers:** US-001/AC-1 "Available products listed", US-001/AC-2 "Empty catalog"

## Files

- `tests/acceptance/catalog.feature`
- `tests/steps/catalog.py`

## Actions to complete

- [x] Write the two catalog acceptance scenarios.
- [X] Connect the fixtures and assertion steps.

## Out of Scope

- Catalog implementation: TASK [TASK-003] Implement catalog list.

## Definition of Done (DoD)

- [x] Both scenarios execute in the acceptance suite.
- [x] The suite reports the expected missing implementation.
