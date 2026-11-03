---
id: US-003
title: Saved card
type: US
relations:
    "EPIC-002":
        title: "Checkout"
        type: EPIC
        relationType: PARENT
        reason: "Parent epic"
    "US-002":
        title: "Card payment"
        type: US
        relationType: BLOCKED_BY
        reason: "A card can be saved only during a card payment"
---

As a Shopper, I want to pay with a card saved during a previous purchase, so that I do not type the card details again.

## Outcome

Returning shoppers pay with their saved card.

## Acceptance Criteria

### AC-1: Pay with saved card

**Given** the shopper saved a card during a previous purchase
**When** the shopper confirms the payment with the saved card
**Then** at the end of processing the order confirmation is shown

### AC-2: No saved card

**Given** the shopper has no saved card
**When** the shopper reaches the payment
**Then** only the card entry is offered

## Out of Scope

- Managing several saved cards: not planned

## INVEST & DoR (Definition of Ready) Check
- [x] **I**ndependent - follows card payment, a real dependency
- [x] **N**egotiable - storage left to the team
- [x] **V**aluable - faster repeat purchases
- [x] **E**stimable - known pattern
- [x] **S**mall - one capability
- [x] **T**estable - binary scenarios
