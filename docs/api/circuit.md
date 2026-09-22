# Orders — circuit breaker

Client: `orders_app.inventory_client.InventoryClient` · Breaker: `distributed_tracing.CircuitBreaker` name `inventory`

## Get circuit stats

`GET /v1/circuit` · fields: `state`, `failures`, `successes`, `opened_at`

## Reset circuit

`POST /v1/circuit/reset` · `{"status":"reset"}` · calls `breaker.reset()`

**Note:** No authentication in current implementation — treat as ops-only in deployments.
