---
id: EPIC-001
title: Discovery
type: EPIC
rank: 10
relations:
  MAP-001:
    title: Online purchase
    type: MAP
    relationType: PARENT
    reason: Discovery is the first activity in the online purchase journey.
---

As a shopper, I want to discover available products, so that I can choose a suitable purchase.

## Outcome

Shoppers find an available item without assistance.

## Scope Boundaries

- In Scope: catalog consultation.
- Out of Scope: recommendations are not planned.

## Acceptance Criteria

### AC-1: Discover an available item

Given an available product, When a shopper explores the catalog, Then they can identify the product and its price.
