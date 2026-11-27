# Research: First online purchase

## Research Questions

- How should card authorization remain safe across retries? See [the Payment Provider finding](#payment-provider).

## Technical Findings

### Payment Provider

- Stripe Payment Intents supports idempotent authorization requests.
- [ADR-0001: Use Stripe Payment Intents for card authorization](../../docs/architecture/adr/0001-use-stripe-payment-intents.md) records the durable provider choice.

## Validity

Recheck if payment-provider requirements or the provider API changes.
