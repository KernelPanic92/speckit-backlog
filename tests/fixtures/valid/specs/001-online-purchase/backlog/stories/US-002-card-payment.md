---
id: US-002
title: Card payment
type: US
relations:
    "EPIC-002":
        title: "Checkout"
        type: EPIC
        relationType: PARENT
        reason: "Parent epic"
    "US-001":
        title: "Catalog list"
        type: US
        relationType: BLOCKED_BY
        reason: "The product to pay for is chosen from the catalog list"
    "SPIKE-001":
        title: "Payment provider"
        type: SPIKE
        relationType: BLOCKED_BY
        reason: "The provider must be chosen before estimating"
---

As a Shopper, I want to pay for a product by card, so that my order is confirmed.

## Outcome

Shoppers pay by Visa or Mastercard and get a confirmation.

## Acceptance Criteria

### AC-1: Successful payment

**Given** the shopper has chosen a product
**When** the shopper confirms the payment with a valid card
**Then** the payment command is disabled and a loading indicator appears
**And** at the end of processing the order confirmation is shown

### AC-2: Payment fails

**Given** the system is unable to process the payment
**When** the shopper confirms the payment
**Then** at the end of processing an error is shown
**And** the payment command is enabled again with the card details still filled in

## Out of Scope

- Saving the card: US [US-003] Saved card

## INVEST & DoR (Definition of Ready) Check
- [x] **I**ndependent - depends only on the catalog list, its entry point
- [x] **N**egotiable - provider chosen by the spike
- [x] **V**aluable - completes the purchase
- [x] **E**stimable - after the spike
- [x] **S**mall - one payment method
- [x] **T**estable - binary scenarios
