---
id: US-003
title: Pay with saved card
type: US
rank: 10
relations:
  FEATURE-003:
    title: Saved payment
    type: FEATURE
    relationType: PARENT
    reason: Reusing a card is the first saved payment slice.
  US-002:
    title: Pay by card
    type: US
    relationType: BLOCKED_BY
    reason: A shopper first needs a successful card payment to save a reusable card.
---

As a returning shopper, I want to pay with my saved card, so that I avoid entering it again.

## Outcome

Returning shoppers complete a purchase without entering a card number.

## Acceptance Criteria

### AC-1: Saved card accepted

```gherkin
@US-003 @AC-1
Scenario: Saved card accepted
  Given my saved card
  When I confirm payment
  Then a loading indicator appears
  And confirmation is disabled until processing completes
  And the indicator disappears
  And I receive an order confirmation
```

### AC-2: Saved card expired

```gherkin
@US-003 @AC-2
Scenario: Saved card expired
  Given my saved card has expired
  When I open payment
  Then I see that the saved card is unavailable
  But I can enter a replacement card
```

## Out of Scope

- Choosing between several saved cards: not planned.
