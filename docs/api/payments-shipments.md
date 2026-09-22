# Orders — payments, shipments, refunds

## List payments

`GET /v1/payments` · limit 500 · `PaymentOut`: id, order_id, amount_cents, status

## List shipments

`GET /v1/shipments` · limit 500 · `ShipmentOut`: id, order_id, carrier, tracking, status

## Create refund

`POST /v1/refunds` · `RefundIn` · `services.request_refund`

| Field | Required | Default | Validation |
|-------|----------|---------|------------|
| order_id | Yes | — | must exist |
| amount_cents | Yes | — | `gt=0`; cannot exceed order.total_cents when total > 0 |
| reason | No | `customer_request` | — |

**Success:** `{"id","status","amount_cents"}` with refund `status` `pending`, order status `refunded`.

| Status | When |
|--------|------|
| 404 | order not found |
| 409 | cannot refund from status / amount exceeds total |
| 400 | amount_cents ≤ 0 (also covered by schema `gt=0` → 422) |
| 422 | validation |

Allowed only if `refunded` is a valid transition from current status (e.g. paid/shipped/delivered).
