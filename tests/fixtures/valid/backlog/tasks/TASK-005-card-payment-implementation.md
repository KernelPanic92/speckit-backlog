---
id: TASK-005
title: Implement card payment
type: TASK
rank: 20
relations:
  US-002:
    title: Pay by card
    type: US
    relationType: PARENT
    reason: Deliver the card payment behavior.
  TASK-004:
    title: Card payment acceptance tests
    type: TASK
    relationType: BLOCKED_BY
    reason: Implement against executable payment scenarios.
---

## Outcome

Authorize payment idempotently and show the order confirmation or retryable decline.

## Files

- `app/payment.py`
- `app/views/payment.html`

## Actions to complete

- [ ] Integrate authorization and order confirmation.
- [ ] Preserve entered data after a decline.

## Out of Scope

- Saved cards: US [US-003] Pay with saved card.

## Definition of Done

- [ ] Card acceptance scenarios pass.
