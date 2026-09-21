# Orders microservice

Creates orders by calling **inventory** behind a **circuit breaker**, with W3C trace propagation.

```bash
pip install -e ".[dev]"
pip install -e ../distributed-tracing
# terminal 1
PORT=8091 python -m inventory_app.app   # from ../inventory
# terminal 2
INVENTORY_URL=http://127.0.0.1:8091 PORT=8092 python -m orders_app.app
curl -X POST http://localhost:8092/orders -H 'content-type: application/json' \
  -d '{"sku":"sku-100","qty":1}'
```

Circuit opens after repeated inventory 5xx → fail-fast `503` with `circuit: open`.

Local-first: `make -C ../platform-ops local-gate REPO=orders`
