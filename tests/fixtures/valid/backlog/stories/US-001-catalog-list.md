---
id: US-001
title: Catalog list
type: US
rank: 10
relations:
  FEATURE-001:
    title: Catalog browsing
    type: FEATURE
    relationType: PARENT
    reason: The catalog list is the first catalog browsing slice.
---

As a shopper, I want to see available products, so that I can compare their prices.

## Outcome

Shoppers can consult current product names and prices.

## Acceptance Criteria

### AC-1: Available products listed

Given available products, When I open the catalog, Then a loading indicator appears and disappears when processing completes, and I see their names and prices.

### AC-2: Empty catalog

Given no available products, When I open the catalog, Then a loading indicator appears and disappears when processing completes, and I see that no products are available.

## Out of Scope

- Product details: not planned.
