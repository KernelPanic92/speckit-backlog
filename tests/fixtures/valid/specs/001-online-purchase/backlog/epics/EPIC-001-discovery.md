---
id: EPIC-001
title: Discovery
type: EPIC
relations:
    "MAP-001":
        title: "Online purchase"
        type: MAP
        relationType: PARENT
        reason: "Backbone Macro-Activity of the map"
---

As a Shopper, I want to find products in the catalog, so that I can choose what to buy.

## Outcome

Shoppers see the products available for sale.

## Scope Boundaries
- **In Scope (what we will do):**
  - [ ] Catalog list
- **Out of Scope (what we will NOT do in this Epic):**
  - [ ] Full-text search (a future Epic)

## Acceptance Criteria

### AC-1: Products are visible

**Given** the catalog has products for sale
**When** the shopper opens the catalog
**Then** the shopper sees the products for sale
