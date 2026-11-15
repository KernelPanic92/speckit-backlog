---
id: MAP-001
title: Online purchase
type: MAP
rank: 10
---

As a shopper, I want to buy a product online, so that I can receive it at home.

## Outcome

Shoppers discover an available product and complete a first card purchase in under three minutes.

## Backbone

| Macro-Activities | 1. EPIC [EPIC-001] Discovery | 2. EPIC [EPIC-002] Checkout |
| --- | --- | --- |
| User Tasks | Browse available products | Pay for a product |

## Walking Skeleton

- [ ] TASK [TASK-001] Purchase pipeline: exercise a static purchase through the deployment pipeline.

## Release Lanes

### Release 1: First purchase by card

Slice by Outcome: a shopper can discover an item and pay once.

- EPIC [EPIC-001] Discovery → FEATURE [FEATURE-001] Catalog browsing
  - US [US-001] Catalog list
- EPIC [EPIC-002] Checkout → FEATURE [FEATURE-002] Card payment
  - US [US-002] Pay by card

### Release 2: Returning shoppers purchase faster

Slice by Persona: returning shoppers reuse their saved card.

- EPIC [EPIC-002] Checkout → FEATURE [FEATURE-003] Saved payment
  - US [US-003] Pay with saved card

## Out of Scope

- Returns: not planned.
