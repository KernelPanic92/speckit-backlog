# Data Model: First online purchase

## Product

| Field | Type | Validation |
| --- | --- | --- |
| `id` | string | Required and unique. |
| `name` | string | Required and non-empty. |
| `price` | decimal | Non-negative in the store currency. |

Products are listed by [US-001, Available products listed](../../backlog/stories/US-001-catalog-list.md#ac-1-available-products-listed). The API shape is defined by the [catalog contract](contracts/catalog-api.yaml).
