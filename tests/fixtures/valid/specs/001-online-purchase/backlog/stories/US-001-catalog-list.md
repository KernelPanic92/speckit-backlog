---
id: US-001
title: Catalog list
type: US
relations:
    "EPIC-001":
        title: "Discovery"
        type: EPIC
        relationType: PARENT
        reason: "Parent epic"
---

As a Shopper, I want to see the list of products for sale, so that I know what I can buy.

## Outcome

The catalog shows every product for sale.

## Acceptance Criteria

### AC-1: List loads

**Given** the catalog has products for sale
**When** the shopper opens the catalog
**Then** a loading indicator appears
**And** at the end of loading the indicator disappears and the products are listed

### AC-2: Empty catalog

**Given** the catalog has no products for sale
**When** the shopper opens the catalog
**Then** at the end of loading the shopper is told that no products are available

## Out of Scope

- Opening the product detail — future story

## INVEST & DoR (Definition of Ready) Check
- [x] **I**ndependent - entry point of the journey
- [x] **N**egotiable - no layout prescribed
- [x] **V**aluable - shoppers see what is on sale
- [x] **E**stimable - known list pattern
- [x] **S**mall - one list
- [x] **T**estable - binary scenarios
