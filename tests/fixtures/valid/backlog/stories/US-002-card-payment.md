---
id: US-002
title: Pay by card
type: US
rank: 10
relations:
  FEATURE-002:
    title: Card payment
    type: FEATURE
    relationType: PARENT
    reason: Paying by card delivers the first card payment slice.
  SPIKE-001:
    title: Payment provider
    type: SPIKE
    relationType: BLOCKED_BY
    reason: Provider behavior must be confirmed before card payment is implemented.
---

As a shopper, I want to pay for my order by card, so that it can be dispatched.

## Outcome

An accepted payment creates exactly one confirmed order.

## Acceptance Criteria

### AC-1: Card accepted

Given a payable order and valid card, When I confirm payment, Then a loading indicator appears and confirmation is disabled until processing completes, then the indicator disappears and I see one order confirmation.

### AC-2: Card declined

Given a card that will be declined, When I confirm payment, Then a loading indicator appears and confirmation is disabled until processing completes, then the indicator disappears and I see an error with my entries retained and confirmation enabled.

## Out of Scope

- Reusing a card: US [US-003] Pay with saved card.
