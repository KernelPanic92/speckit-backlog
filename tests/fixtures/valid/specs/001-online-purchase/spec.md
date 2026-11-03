---
id: MAP-001
title: Online purchase
type: MAP
---

As a Shopper, I want to buy a product from the online catalog, so that I receive it at home without visiting a store.

## Outcome

A shopper finds a product, pays for it by card and gets a confirmation.

## Backbone

| Macro-Activities (Epics) | 1. EPIC [EPIC-001] Discovery | 2. EPIC [EPIC-002] Checkout |
|:---|:---|:---|
| **User Tasks (Actions)** | - Browse the catalog | - Pay by card<br>- Save the card |

## Walking Skeleton

- [ ] **TASK [TASK-001] Discovery:** Static list of 3 products from the database

## Release Lanes

### Release 1: First purchase by card
*A shopper browses the catalog and pays by card. Slicing by Outcome.*
* **Goal:** Enable the first complete purchase
* **Metrics:** 10 purchases without errors
* **1. EPIC [EPIC-001] Discovery**
  * US [US-001] Catalog list
* **2. EPIC [EPIC-002] Checkout**
  * US [US-002] Card payment

### Release 2: Faster repeat purchases
*Returning shoppers pay without typing their card again. Slicing Necessity vs Richness.*
* **Goal:** Shorter checkout for returning shoppers
* **Metrics:** Checkout time -30% for returning shoppers
* **2. EPIC [EPIC-002] Checkout**
  * US [US-003] Saved card

## Out of Scope

- Marketplace sellers: not planned

## DoR (Definition of Ready) Check
- [x] Narrative - browse, then pay
- [x] Vertical - every lane crosses the Backbone
- [x] Gravity - stories ordered by necessity
- [x] Functional - describes the experience
- [x] Walking Skeleton vs MVP - the skeleton is a static list
- [x] Lane Outcomes - lanes titled with Outcomes
- [x] Elevator Pitch - under 60 seconds

## Spec Context

**Mode**: map

**Root PBI**: MAP [MAP-001] Online purchase

**Product context**: `.specify/memory/product.md` (Personas, Ubiquitous Language)

**Status**: Draft

## Backlog Index

### Release 1: First purchase by card

- [EPIC [EPIC-001] Discovery](backlog/epics/EPIC-001-discovery.md)
- [EPIC [EPIC-002] Checkout](backlog/epics/EPIC-002-checkout.md)
- [US [US-001] Catalog list](backlog/stories/US-001-catalog-list.md)
- [US [US-002] Card payment](backlog/stories/US-002-card-payment.md)
- [SPIKE [SPIKE-001] Payment provider](backlog/spikes/SPIKE-001-payment-provider.md)

### Release 2: Faster repeat purchases

- [US [US-003] Saved card](backlog/stories/US-003-saved-card.md)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Shoppers complete a first purchase in under 3 minutes

## Open Questions

- [x] Q1: Which card networks are accepted? — affects US [US-002] Card payment → see Clarifications

## Clarifications

### Session 2026-11-02

- Q: Which card networks are accepted? → A: Visa and Mastercard
