# Quickstart: First online purchase

## Prerequisites

- Python environment configured with test dependencies.
- `PAYMENT_PROVIDER=stub` for local acceptance runs.

## Verification

Run the feature acceptance suite:

```sh
uv run pytest tests/acceptance/test_purchase.py
```

Smoke-check the [catalog API contract](contracts/catalog-api.yaml) with `uv run pytest tests/acceptance/test_catalog_api.py -q`.
