# Orders — customers

## List / create / get

| Method | URL | Handler | Notes |
|--------|-----|---------|-------|
| GET | `/v1/customers` | `list_customers` | all rows |
| POST | `/v1/customers` | `create_customer` | `201` · `CustomerCreate` |
| GET | `/v1/customers/{customer_id}` | `get_customer` | **404** if missing |

**CustomerCreate:** `email` (string, required), `name` (string, required)  
**CustomerOut:** `id`, `email`, `name`

**DB:** Model `Customer`; email column is unique at DB level — duplicate insert may surface as `500` if not caught (not explicitly mapped to 409 in handler). Not explicitly enforced as 409 in current implementation.
