---
id: TASK-004
title: Card payment acceptance tests
type: TASK
rank: 10
relations:
  US-002:
    title: Pay by card
    type: US
    relationType: PARENT
    reason: Automate accepted and declined card payment scenarios.
---

## Outcome

Verify successful and declined payments without calling the live provider.

**Covers:** US-002/AC-1 "Card accepted", US-002/AC-2 "Card declined"

## Files

- `tests/acceptance/payment.feature`
- `tests/steps/payment.py`

## Actions to complete

- [ ] Create provider stubs and payment scenarios.

## Out of Scope

- Provider integration: TASK [TASK-005] Implement card payment.

## Definition of Done

- [ ] Scenarios run deterministically with the provider stubs.
