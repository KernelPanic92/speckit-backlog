---
id: EPIC-002
title: Checkout
type: EPIC
relations:
    "MAP-001":
        title: "Online purchase"
        type: MAP
        relationType: PARENT
        reason: "Backbone Macro-Activity of the map"
---

As a Shopper, I want to pay for the products I chose, so that the order is confirmed.

## Outcome

Shoppers pay and receive a confirmation.

## Scope Boundaries
- **In Scope (what we will do):**
  - [ ] Card payment
- **Out of Scope (what we will NOT do in this Epic):**
  - [ ] PayPal (a future Epic)

## Acceptance Criteria

### AC-1: Paid order is confirmed

**Given** the shopper has chosen a product
**When** the shopper pays successfully
**Then** the order is confirmed
