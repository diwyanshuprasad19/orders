# Orders — ops

## Health

`GET /health` · returns `status`, `service`, and `circuit` (`state`, `failures` from breaker stats).

## Ready

`GET /ready` · DB `SELECT 1` · `{"status":"ready"}`

## Metrics / telemetry / seed

- `GET /metrics` — Prometheus text  
- `GET /v1/telemetry` — `telemetry_status()` dict  
- `POST /v1/seed` — `seed_demo` creates demo customers; returns `{"customers_created": <int>}`

Files: `src/orders_app/app.py`, `src/orders_app/seed.py`
