---
id: FEATURE-002
title: Card payment
type: FEATURE
rank: 10
relations:
  EPIC-002:
    title: Checkout
    type: EPIC
    relationType: PARENT
    reason: Card payment enables the first checkout.
---

As a shopper, I want to purchase with a card, so that my order can be dispatched.

## Outcome

Ten first-time shoppers complete a card purchase without assistance.

## Constraints

- Payment details must not appear in order logs.

## Out of Scope

- Reusing a card: FEATURE [FEATURE-003] Saved payment.
