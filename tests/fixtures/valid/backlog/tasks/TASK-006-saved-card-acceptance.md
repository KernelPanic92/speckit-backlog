---
id: TASK-006
title: Saved card acceptance tests
type: TASK
rank: 10
relations:
  US-003:
    title: Pay with saved card
    type: US
    relationType: PARENT
    reason: Automate saved-card acceptance scenarios.
---

## Outcome

Verify accepted and expired saved-card behavior.

**Covers:** US-003/AC-1 "Saved card accepted", US-003/AC-2 "Saved card expired"

## Files

- `tests/acceptance/saved-card.feature`

## Actions to complete

- [ ] Write saved-card acceptance scenarios and fixtures.

## Out of Scope

- Provider token persistence: TASK [TASK-007] Implement saved card payment.

## Definition of Done

- [ ] Acceptance scenarios execute without a live provider.
