# Implementation Plan: First online purchase

## Summary

Ship catalog browsing and card payment for the first purchase.

## Technical Context

Catalog reads use the product model in [the data model](data-model.md#product). Card authorization follows [ADR-0001: Use Stripe Payment Intents](../../docs/architecture/adr/0001-use-stripe-payment-intents.md). Evidence is in [payment provider research](research.md#payment-provider).

## Constitution Check

- Keep payment credentials outside the purchase service.

## Project Structure

- `app/catalog/` — catalog query and product mapping.
- `app/payments/` — payment intent adapter.
- `tests/acceptance/` — story acceptance suite.
- [Catalog API contract](contracts/catalog-api.yaml) — catalog boundary.

## Delivery Slices

- Catalog list: [US-001](../../backlog/stories/US-001-catalog-list.md); verify with [the quickstart](quickstart.md#verification).
- Card payment: [US-002](../../backlog/stories/US-002-card-payment.md); follow the payment decision in [ADR-0001](../../docs/architecture/adr/0001-use-stripe-payment-intents.md).
