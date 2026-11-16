---
id: BUG-001
title: Currency label
type: BUG
rank: 10
relations:
  FEATURE-001:
    title: Catalog browsing
    type: FEATURE
    relationType: PARENT
    reason: Correct the catalog currency label in the existing storefront.
---

## Reproduction

Open the legacy storefront with the store currency set to EUR: its label still says USD.

## Expected Behavior

The displayed label matches the configured store currency.
