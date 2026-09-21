"""Orders API edge cases — remote inventory failures, circuit, state machine, telemetry."""

from __future__ import annotations

import os

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from orders_app.app import create_app
from orders_app.db import Base, get_db
from orders_app.inventory_client import InventoryClient
from orders_app.seed import seed_demo


class FakeTransport(httpx.BaseTransport):
    def __init__(self) -> None:
        self.mode = "ok"  # ok | connect | timeout | upstream_5xx | upstream_404 | bad_json
        self.calls = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.calls += 1
        if self.mode == "connect":
            raise httpx.ConnectError("connection refused")
        if self.mode == "timeout":
            raise httpx.ReadTimeout("timed out")
        if self.mode == "upstream_5xx":
            return httpx.Response(502, json={"error": "bad_gateway"})
        if self.mode == "upstream_404" or (
            self.mode == "ok" and request.url.path.startswith("/stock/UNKNOWN")
        ):
            return httpx.Response(404, json={"error": "not_found"})
        if self.mode == "bad_json":
            return httpx.Response(200, content=b"{not-json")
        if request.url.path.startswith("/stock/"):
            return httpx.Response(
                200,
                json={"sku": "WIDGET-1", "quantity": 100, "reserved": 0, "available": 100},
            )
        if request.url.path == "/reserve":
            return httpx.Response(
                200,
                json={
                    "sku": "WIDGET-1",
                    "reserved": 1,
                    "available": 99,
                    "status": "reserved",
                    "reservation_id": "r1",
                },
            )
        return httpx.Response(404, json={"error": "nope"})


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def _get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    transport = FakeTransport()
    inv = InventoryClient(
        base_url="http://inventory.test",
        failure_threshold=2,
        recovery_timeout=60,
        transport=transport,
    )
    app = create_app(inventory=inv)
    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        db = Session()
        seed_demo(db)
        db.close()
        c.transport_fake = transport  # type: ignore
        c.inv = inv  # type: ignore
        yield c


def test_create_order(client):
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 100})
    assert r.status_code == 201
    assert r.json()["status"] == "confirmed"


def test_customers_seeded(client):
    assert len(client.get("/v1/customers").json()) >= 5


def test_telemetry_safe(client):
    r = client.get("/v1/telemetry")
    assert r.status_code == 200
    assert "password" not in r.text.lower()


def test_validation_qty(client):
    assert client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 0}).status_code == 422
    assert client.post("/v1/orders", json={"sku": "", "qty": 1}).status_code == 422


def test_remote_connect_error_then_circuit(client):
    client.transport_fake.mode = "connect"  # type: ignore
    for _ in range(2):
        r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
        assert r.status_code in {502, 503}
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert r.status_code == 503
    assert client.get("/v1/circuit").json()["state"] == "open"


def test_remote_timeout(client):
    client.transport_fake.mode = "timeout"  # type: ignore
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert r.status_code in {502, 503, 504}


def test_upstream_5xx(client):
    client.transport_fake.mode = "upstream_5xx"  # type: ignore
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert r.status_code in {502, 503}


def test_unknown_sku_from_inventory(client):
    r = client.post("/v1/orders", json={"sku": "UNKNOWN", "qty": 1})
    assert r.status_code == 404


def test_circuit_reset(client):
    client.transport_fake.mode = "connect"  # type: ignore
    for _ in range(2):
        client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert client.get("/v1/circuit").json()["state"] == "open"
    assert client.post("/v1/circuit/reset").status_code == 200
    assert client.get("/v1/circuit").json()["state"] == "closed"
    client.transport_fake.mode = "ok"  # type: ignore
    ok = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert ok.status_code == 201


def test_invalid_status_transition(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    # confirmed -> delivered is invalid (must go through paid/shipped)
    bad = client.patch(f"/v1/orders/{oid}/status", json={"status": "delivered"})
    assert bad.status_code == 409


def test_pay_ship_events(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/pay", json={}).status_code == 200
    assert client.post(f"/v1/orders/{oid}/ship", json={"carrier": "UPS"}).status_code == 200
    events = client.get(f"/v1/orders/{oid}/events").json()
    types = {e["event_type"] for e in events}
    assert "created" in types
    assert "paid" in types
    assert "shipped" in types


def test_cannot_pay_cancelled(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 200
    assert client.post(f"/v1/orders/{oid}/pay", json={}).status_code == 409


def test_cannot_ship_cancelled(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 200
    assert client.post(f"/v1/orders/{oid}/ship", json={"carrier": "UPS"}).status_code == 409


def test_refund_exceeds_total(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/pay", json={}).status_code == 200
    r = client.post("/v1/refunds", json={"order_id": oid, "amount_cents": 9999})
    assert r.status_code == 409


def test_remote_bad_json(client):
    client.transport_fake.mode = "bad_json"  # type: ignore
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert r.status_code in {502, 503}


def test_empty_json_body(client):
    r = client.post("/v1/orders", content=b"{}", headers={"content-type": "application/json"})
    assert r.status_code in {400, 422}
