from __future__ import annotations

import json

from sqlalchemy.orm import Session

from orders_app import models
from orders_app.inventory_client import CircuitOpenError, InventoryClient


class OrderError(Exception):
    def __init__(self, message: str, code: int = 400) -> None:
        self.code = code
        super().__init__(message)


def add_event(db: Session, order: models.Order, event_type: str, payload: dict | None = None):
    db.add(
        models.OrderEvent(
            order_id=order.id,
            event_type=event_type,
            payload=json.dumps(payload or {}),
        )
    )


def create_order(
    db: Session,
    client: InventoryClient,
    *,
    sku: str,
    qty: int,
    customer_id: str | None,
    unit_price_cents: int,
) -> models.Order:
    try:
        stock = client.get_stock(sku)
    except CircuitOpenError as e:
        raise OrderError(
            f"inventory_unavailable retry_after={e.retry_after}", 503
        ) from e
    except Exception as e:
        raise OrderError(f"inventory_error: {e}", 502) from e

    if stock.get("error") == "not_found" or stock.get("http_status") == 404:
        raise OrderError("unknown_sku", 404)
    if int(stock.get("available", 0)) < qty:
        raise OrderError("insufficient_stock", 409)

    try:
        reserved = client.reserve(sku, qty)
    except CircuitOpenError as e:
        raise OrderError(
            f"inventory_unavailable retry_after={e.retry_after}", 503
        ) from e
    except Exception as e:
        raise OrderError(f"inventory_error: {e}", 502) from e

    if int(reserved.get("http_status", 200)) >= 400:
        raise OrderError(reserved.get("error", "reserve_failed"), int(reserved["http_status"]))

    order = models.Order(
        customer_id=customer_id,
        sku=sku,
        qty=qty,
        status="confirmed",
        reservation_id=reserved.get("reservation_id"),
        total_cents=unit_price_cents * qty,
    )
    db.add(order)
    db.flush()
    add_event(db, order, "created", {"sku": sku, "qty": qty})
    add_event(db, order, "inventory_reserved", {"reservation_id": order.reservation_id})
    db.commit()
    db.refresh(order)
    return order


VALID_TRANSITIONS = {
    "pending": {"confirmed", "cancelled"},
    "confirmed": {"paid", "cancelled", "shipped"},
    "paid": {"shipped", "refunded", "cancelled"},
    "shipped": {"delivered", "refunded"},
    "delivered": {"refunded"},
    "cancelled": set(),
    "refunded": set(),
}


def update_status(db: Session, order: models.Order, new_status: str) -> models.Order:
    allowed = VALID_TRANSITIONS.get(order.status, set())
    if new_status not in allowed and new_status != order.status:
        raise OrderError(f"invalid transition {order.status}->{new_status}", 409)
    order.status = new_status
    add_event(db, order, "status_changed", {"status": new_status})
    db.commit()
    db.refresh(order)
    return order
