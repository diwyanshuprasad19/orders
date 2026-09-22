# Orders service API index

Framework: **FastAPI** · App: `orders_app.app:create_app` · Default port: `8092` · Outbound: inventory via `InventoryClient` + `CircuitBreaker`

Interactive OpenAPI at runtime: `GET <BASE_URL>/docs`

Auth: **Not explicitly enforced in current implementation**.

| Method | Endpoint | Purpose | Auth | Doc |
|--------|----------|---------|------|-----|
| GET | `/health` | Liveness + circuit stats | Public | [ops.md](ops.md) |
| GET | `/ready` | DB ready | Public | [ops.md](ops.md) |
| GET | `/metrics` | Prometheus | Public | [ops.md](ops.md) |
| GET | `/v1/telemetry` | OTel status | Public | [ops.md](ops.md) |
| POST | `/v1/seed` | Seed customers | Public | [ops.md](ops.md) |
| GET | `/v1/circuit` | Breaker stats | Public | [circuit.md](circuit.md) |
| POST | `/v1/circuit/reset` | Reset breaker | Public | [circuit.md](circuit.md) |
| GET | `/v1/orders` | List orders | Public | [orders.md](orders.md) |
| POST | `/v1/orders` | Create order (reserves inventory) | Public | [orders.md](orders.md) |
| GET | `/v1/orders/{order_id}` | Get order | Public | [orders.md](orders.md) |
| PATCH | `/v1/orders/{order_id}/status` | Status transition | Public | [orders.md](orders.md) |
| POST | `/v1/orders/{order_id}/cancel` | Cancel | Public | [orders.md](orders.md) |
| POST | `/v1/orders/{order_id}/pay` | Capture payment | Public | [orders.md](orders.md) |
| POST | `/v1/orders/{order_id}/ship` | Create shipment | Public | [orders.md](orders.md) |
| GET | `/v1/orders/{order_id}/events` | Order events | Public | [orders.md](orders.md) |
| GET | `/v1/customers` | List customers | Public | [customers.md](customers.md) |
| POST | `/v1/customers` | Create customer | Public | [customers.md](customers.md) |
| GET | `/v1/customers/{customer_id}` | Get customer | Public | [customers.md](customers.md) |
| GET | `/v1/payments` | List payments | Public | [payments-shipments.md](payments-shipments.md) |
| GET | `/v1/shipments` | List shipments | Public | [payments-shipments.md](payments-shipments.md) |
| POST | `/v1/refunds` | Request refund | Public | [payments-shipments.md](payments-shipments.md) |
| POST | `/orders` | Legacy create | Public | [legacy.md](legacy.md) |
| GET | `/orders/{order_id}` | Legacy get | Public | [legacy.md](legacy.md) |

Index from routes in `src/orders_app/app.py`.
