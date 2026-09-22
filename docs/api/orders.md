# Orders — orders lifecycle

Schemas: `src/orders_app/schemas.py` · Service: `src/orders_app/services.py` · App: `src/orders_app/app.py` · Remote: `InventoryClient`

## Status state machine (`VALID_TRANSITIONS`)

| From | Allowed next |
|------|----------------|
| pending | confirmed, cancelled |
| confirmed | paid, cancelled, shipped |
| paid | shipped, refunded, cancelled |
| shipped | delivered, refunded |
| delivered | refunded |
| cancelled | — |
| refunded | — |

Create order sets status **`confirmed`** after successful inventory reserve.

---

## List orders

`GET /v1/orders` · limit 500 · `list[OrderOut]`

| Field | Type | Nullable |
|-------|------|----------|
| id | string | No |
| sku | string | No |
| qty | integer | No |
| status | string | No |
| customer_id | string | Yes |
| reservation_id | string | Yes |
| total_cents | integer | No |
| created_at | datetime | Yes |

---

## Create order

**Purpose:** Check inventory stock, reserve qty, persist order.

| | |
|--|--|
| Method | `POST` |
| URL | `/v1/orders` |
| Status | `201` |
| Handler | `create_order` |
| Service | `services.create_order` |
| Request | `OrderCreate` |

**OrderCreate**

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| sku | string | Yes | — | min 1, max 64 |
| qty | integer | Yes | — | `gt=0` |
| customer_id | string | No | null | — |
| unit_price_cents | integer | No | `0` | — |

**Sample:**
```json
{"sku":"WIDGET-1","qty":1,"unit_price_cents":1200}
```

**curl:**
```bash
curl --request POST \
  --url '<BASE_URL>/v1/orders' \
  --header 'Content-Type: application/json' \
  --data '{"sku":"WIDGET-1","qty":1,"unit_price_cents":1200}'
```

**Success `201`:** `OrderOut` with `status` typically `confirmed`, `total_cents = unit_price_cents * qty`.

**Errors (from `OrderError` / HTTPException)**

| Status | Condition |
|--------|-----------|
| 404 | unknown_sku |
| 409 | insufficient_stock |
| 502 | inventory_error (connect/timeout/5xx/bad JSON, etc.) |
| 503 | inventory_unavailable (circuit open) |
| 422 | validation |

**External dependency:** Inventory HTTP (`INVENTORY_URL`, default `http://127.0.0.1:8091`) via `/stock/{sku}` and `/reserve`.

**DB:** Creates `Order`, `OrderEvent` (`created`, `inventory_reserved`).

**Internal flow:** FastAPI → `create_order` → `InventoryClient.get_stock` → `reserve` → persist → 201.

**Idempotency:** Not explicitly enforced in current implementation (duplicate POSTs create multiple orders).

---

## Get order

`GET /v1/orders/{order_id}` · **404** not found · **200** `OrderOut`

---

## Patch status

`PATCH /v1/orders/{order_id}/status` · body `{"status":"<new>"}` · `services.update_status`

**409** invalid transition · **404** missing order · **200** `OrderOut`

---

## Cancel

`POST /v1/orders/{order_id}/cancel` · transitions to `cancelled` if allowed · **409** if not.

---

## Pay

`POST /v1/orders/{order_id}/pay` · `PayIn` · `services.capture_payment`

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| amount_cents | No | order.total_cents | Must be ≥0; cannot exceed total when total > 0 |
| provider_ref | No | null | Optional |

Allowed only if `paid` ∈ transitions from current status (e.g. from `confirmed`).  
**409** cannot pay / amount exceeds total · Creates `Payment`, sets status `paid`.

---

## Ship

`POST /v1/orders/{order_id}/ship` · `ShipIn` · `services.create_shipment`

| Field | Default |
|-------|---------|
| carrier | `"UPS"` |
| tracking | null |

**409** if cannot ship from status · Creates `Shipment`, status `shipped`.

---

## Order events

`GET /v1/orders/{order_id}/events` · `list[EventOut]` (`id`, `event_type`, `payload`, `created_at`)
