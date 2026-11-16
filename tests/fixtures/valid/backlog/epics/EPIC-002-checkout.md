---
id: EPIC-002
title: Checkout
type: EPIC
rank: 20
relations:
  MAP-001:
    title: Online purchase
    type: MAP
    relationType: PARENT
    reason: Checkout closes the online purchase journey.
---

As a shopper, I want to pay for my purchase, so that the order can be dispatched.

## Outcome

Shoppers receive an order confirmation after payment.

## Scope Boundaries

- In Scope: card purchase and saved-card purchase.
- Out of Scope: bank transfers are not planned.

## Acceptance Criteria

### AC-1: Complete a purchase

Given a payable order, When a shopper pays successfully, Then they receive its confirmation.
