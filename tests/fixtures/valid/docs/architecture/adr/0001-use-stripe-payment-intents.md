# ADR-0001: Use Stripe Payment Intents for card authorization

| **Status** | Accepted |
| **Supersedes** | None |
| **Origin** | [Payment provider research](../../../specs/001-mvp-purchase/research.md#payment-provider) |
| **Tags** | payments, provider |

## Context

The first purchase needs card authorization with retry-safe requests.

## Decision Drivers

- Prevent duplicate authorization on client retries.
- Keep card data out of the purchase service.

## Decision

Use Stripe Payment Intents for card authorization and persist the provider intent ID.

## Consequences

### Positive

- The provider owns sensitive card entry and authorization lifecycle.

### Negative

- Provider outages can prevent new purchases.
- Payment behavior depends on Stripe's API and account availability.

## References

- [Payment plan](../../../specs/001-mvp-purchase/plan.md#technical-context)
