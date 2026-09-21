# orders

Production orders microservice (FastAPI + Postgres/Alembic + circuit breaker + OTel).

## APIs (≥20)
- `GET /health` — liveness\n- `GET /ready` — readiness\n- `GET /v1/orders` — list orders\n- `POST /v1/orders` — create order (CB→inventory)\n- `GET /v1/orders/{id}` — get order\n- `PATCH /v1/orders/{id}/status` — update status\n- `POST /v1/orders/{id}/cancel` — cancel\n- `POST /v1/orders/{id}/pay` — capture payment\n- `POST /v1/orders/{id}/ship` — ship\n- `GET /v1/customers` — list customers\n- `POST /v1/customers` — create customer\n- `GET /v1/customers/{id}` — get customer\n- `GET /v1/payments` — list payments\n- `GET /v1/shipments` — list shipments\n- `POST /v1/refunds` — create refund\n- `GET /v1/circuit` — circuit breaker stats\n- `POST /v1/circuit/reset` — reset breaker\n- `GET /v1/orders/{id}/events` — order event log\n- `POST /v1/seed` — seed demo data\n- `GET /v1/telemetry` — otel status\n- `GET /metrics` — prometheus text

```bash
pip install -e ".[dev]"
pip install -e ../distributed-tracing
alembic upgrade head
INVENTORY_URL=http://127.0.0.1:8091 PORT=8092 python -m orders_app.app
```
