from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from sqlalchemy import select, text
from sqlalchemy.orm import Session

_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from orders_app import models, schemas, services
from orders_app.db import get_db
from orders_app.inventory_client import InventoryClient
from orders_app.seed import seed_demo
from orders_app.settings import get_settings

try:
    from distributed_tracing import (
        configure_tracing,
        instrument_fastapi,
        telemetry_status,
    )
    from distributed_tracing.httpx_otel import instrument_httpx
    from distributed_tracing.logging_otel import configure_logging_otel
    from distributed_tracing.sqlalchemy_otel import instrument_sqlalchemy

    from orders_app.db import engine as _engine
except ImportError:  # pragma: no cover
    configure_tracing = None
    instrument_fastapi = None
    telemetry_status = lambda: {"tracing_configured": False}  # type: ignore
    instrument_httpx = lambda: None  # type: ignore
    instrument_sqlalchemy = lambda engine=None: None  # type: ignore
    configure_logging_otel = lambda: None  # type: ignore
    _engine = None

REQ = Counter("orders_http_requests_total", "HTTP requests", ["route", "code"])
settings = get_settings()
_inventory = InventoryClient()


def create_app(inventory: InventoryClient | None = None) -> FastAPI:
    app = FastAPI(title="Orders Service", version="0.2.0")
    client = inventory or _inventory
    app.state.inventory = client

    if configure_tracing:
        os.environ.setdefault("OTEL_SERVICE_NAME", settings.otel_service_name)
        os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", settings.otel_exporter_otlp_endpoint)
        configure_tracing(settings.otel_service_name)
        configure_logging_otel()
        instrument_httpx()
        if _engine is not None:
            instrument_sqlalchemy(_engine)
        instrument_fastapi(app, service_name=settings.otel_service_name)

    @app.get("/health")
    def health():
        st = client.breaker.stats()
        return {
            "status": "ok",
            "service": "orders",
            "circuit": {"state": st.state.value, "failures": st.failures},
        }

    @app.get("/ready")
    def ready(db: Session = Depends(get_db)):
        db.execute(text("SELECT 1"))
        return {"status": "ready"}

    @app.get("/v1/orders", response_model=list[schemas.OrderOut])
    def list_orders(db: Session = Depends(get_db)):
        return db.scalars(select(models.Order).limit(500)).all()

    @app.post("/v1/orders", response_model=schemas.OrderOut, status_code=201)
    def create_order(body: schemas.OrderCreate, db: Session = Depends(get_db)):
        try:
            order = services.create_order(
                db,
                client,
                sku=body.sku,
                qty=body.qty,
                customer_id=body.customer_id,
                unit_price_cents=body.unit_price_cents,
            )
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e
        return order

    @app.get("/v1/orders/{order_id}", response_model=schemas.OrderOut)
    def get_order(order_id: str, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        return order

    @app.patch("/v1/orders/{order_id}/status", response_model=schemas.OrderOut)
    def patch_status(order_id: str, body: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        try:
            return services.update_status(db, order, body.status)
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e

    @app.post("/v1/orders/{order_id}/cancel", response_model=schemas.OrderOut)
    def cancel(order_id: str, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        try:
            return services.update_status(db, order, "cancelled")
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e

    @app.post("/v1/orders/{order_id}/pay", response_model=schemas.PaymentOut)
    def pay(order_id: str, body: schemas.PayIn, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        try:
            return services.capture_payment(
                db,
                order,
                amount_cents=body.amount_cents,
                provider_ref=body.provider_ref,
            )
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e

    @app.post("/v1/orders/{order_id}/ship", response_model=schemas.ShipmentOut)
    def ship(order_id: str, body: schemas.ShipIn, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        try:
            return services.create_shipment(
                db, order, carrier=body.carrier, tracking=body.tracking
            )
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e

    @app.get("/v1/customers", response_model=list[schemas.CustomerOut])
    def list_customers(db: Session = Depends(get_db)):
        return db.scalars(select(models.Customer)).all()

    @app.post("/v1/customers", response_model=schemas.CustomerOut, status_code=201)
    def create_customer(body: schemas.CustomerCreate, db: Session = Depends(get_db)):
        row = models.Customer(email=body.email, name=body.name)
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @app.get("/v1/customers/{customer_id}", response_model=schemas.CustomerOut)
    def get_customer(customer_id: str, db: Session = Depends(get_db)):
        row = db.get(models.Customer, customer_id)
        if not row:
            raise HTTPException(404, "not found")
        return row

    @app.get("/v1/payments", response_model=list[schemas.PaymentOut])
    def list_payments(db: Session = Depends(get_db)):
        return db.scalars(select(models.Payment).limit(500)).all()

    @app.get("/v1/shipments", response_model=list[schemas.ShipmentOut])
    def list_shipments(db: Session = Depends(get_db)):
        return db.scalars(select(models.Shipment).limit(500)).all()

    @app.post("/v1/refunds")
    def create_refund(body: schemas.RefundIn, db: Session = Depends(get_db)):
        order = db.get(models.Order, body.order_id)
        if not order:
            raise HTTPException(404, "order not found")
        try:
            ref = services.request_refund(
                db, order, amount_cents=body.amount_cents, reason=body.reason
            )
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e
        return {"id": ref.id, "status": ref.status, "amount_cents": ref.amount_cents}

    @app.get("/v1/circuit")
    def circuit():
        st = client.breaker.stats()
        return {
            "state": st.state.value,
            "failures": st.failures,
            "successes": st.successes,
            "opened_at": st.opened_at,
        }

    @app.post("/v1/circuit/reset")
    def circuit_reset():
        client.breaker.reset()
        return {"status": "reset"}

    @app.get("/v1/orders/{order_id}/events", response_model=list[schemas.EventOut])
    def order_events(order_id: str, db: Session = Depends(get_db)):
        return db.scalars(
            select(models.OrderEvent).where(models.OrderEvent.order_id == order_id)
        ).all()

    @app.post("/v1/seed")
    def seed(db: Session = Depends(get_db)):
        return seed_demo(db)

    @app.get("/v1/telemetry")
    def telemetry():
        return telemetry_status()

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    # legacy alias
    @app.post("/orders", status_code=201)
    def legacy_create(body: schemas.OrderCreate, db: Session = Depends(get_db)):
        try:
            order = services.create_order(
                db,
                client,
                sku=body.sku,
                qty=body.qty,
                customer_id=body.customer_id,
                unit_price_cents=body.unit_price_cents,
            )
        except services.OrderError as e:
            raise HTTPException(e.code, str(e)) from e
        return {
            "order_id": order.id,
            "sku": order.sku,
            "qty": order.qty,
            "status": order.status,
        }

    @app.get("/orders/{order_id}")
    def legacy_get(order_id: str, db: Session = Depends(get_db)):
        order = db.get(models.Order, order_id)
        if not order:
            raise HTTPException(404, "not found")
        return {
            "order_id": order.id,
            "sku": order.sku,
            "qty": order.qty,
            "status": order.status,
        }

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", str(settings.port))),
        reload=False,
    )


if __name__ == "__main__":
    main()
