---
id: TASK-007
title: Implement saved card payment
type: TASK
rank: 20
relations:
  US-003:
    title: Pay with saved card
    type: US
    relationType: PARENT
    reason: Deliver saved-card purchase behavior.
  TASK-006:
    title: Saved card acceptance tests
    type: TASK
    relationType: BLOCKED_BY
    reason: Implement against executable saved-card scenarios.
---

## Outcome

Use an owner-scoped provider token for a returning shopper's purchase.

## Files

- `app/saved_payment.py`

## Actions to complete

- [ ] Resolve the shopper's saved token and handle expiry.

## Out of Scope

- Multiple saved cards: not planned.

## Definition of Done

- [ ] Saved-card acceptance scenarios pass.
