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

```gherkin
@US-001 @AC-1
Scenario: Available products listed
  Given available products
  When I open the catalog
  Then a loading indicator appears
  And the indicator disappears when processing completes
  And I see their names and prices
```

### AC-2: Empty catalog

```gherkin
@US-001 @AC-2
Scenario: Empty catalog
  Given no available products
  When I open the catalog
  Then a loading indicator appears
  And the indicator disappears when processing completes
  And I see that no products are available
```

## Out of Scope

- Product details: not planned.
