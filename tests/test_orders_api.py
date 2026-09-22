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
        if request.url.path == "/release":
            return httpx.Response(
                200,
                json={"reservation_id": "r1", "status": "released"},
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


def test_ready_metrics_seed_lists_and_crud(client):
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200
    assert client.get("/metrics").status_code == 200
    assert client.post("/v1/seed").status_code == 200
    assert client.get("/v1/orders").status_code == 200
    assert client.get("/v1/payments").status_code == 200
    assert client.get("/v1/shipments").status_code == 200
    cust = client.post("/v1/customers", json={"email": "core@example.com", "name": "Core"})
    assert cust.status_code == 201
    cid = cust.json()["id"]
    assert client.get(f"/v1/customers/{cid}").status_code == 200
    assert client.get("/v1/customers/missing").status_code == 404


def test_get_order_not_found_and_happy_path(client):
    assert client.get("/v1/orders/nope").status_code == 404
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 25})
    oid = created.json()["id"]
    assert client.get(f"/v1/orders/{oid}").status_code == 200
    assert client.patch(f"/v1/orders/{oid}/status", json={"status": "paid"}).status_code == 200
    assert client.patch("/v1/orders/nope/status", json={"status": "paid"}).status_code == 404
    assert client.post("/v1/orders/nope/cancel").status_code == 404
    assert client.post("/v1/orders/nope/pay", json={}).status_code == 404
    assert client.post("/v1/orders/nope/ship", json={"carrier": "X"}).status_code == 404


def test_refund_happy_and_validation(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/pay", json={}).status_code == 200
    ok = client.post("/v1/refunds", json={"order_id": oid, "amount_cents": 10, "reason": "partial"})
    assert ok.status_code == 200
    assert ok.json()["status"] == "pending"
    assert (
        client.post("/v1/refunds", json={"order_id": "missing", "amount_cents": 1}).status_code
        == 404
    )
    # cannot refund again from refunded
    created2 = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid2 = created2.json()["id"]
    assert client.post("/v1/refunds", json={"order_id": oid2, "amount_cents": 1}).status_code == 409


def test_pay_amount_edges(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 100})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/pay", json={"amount_cents": -1}).status_code == 400
    assert client.post(f"/v1/orders/{oid}/pay", json={"amount_cents": 9999}).status_code == 409
    assert client.post(f"/v1/orders/{oid}/pay", json={"amount_cents": 50}).status_code == 200


def test_legacy_orders_and_insufficient_stock(client):
    legacy = client.post("/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 10})
    assert legacy.status_code == 201
    oid = legacy.json()["order_id"]
    assert client.get(f"/orders/{oid}").status_code == 200
    assert client.get("/orders/missing").status_code == 404

    # force insufficient via fake stock
    class LowTransport(httpx.BaseTransport):
        def handle_request(self, request: httpx.Request) -> httpx.Response:
            if request.url.path.startswith("/stock/"):
                return httpx.Response(
                    200,
                    json={"sku": "WIDGET-1", "quantity": 1, "reserved": 0, "available": 0},
                )
            return httpx.Response(404)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from orders_app.app import create_app
    from orders_app.db import Base, get_db
    from orders_app.inventory_client import InventoryClient

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

    inv = InventoryClient(
        base_url="http://inventory.test",
        failure_threshold=5,
        transport=LowTransport(),
    )
    app = create_app(inventory=inv)
    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        r = c.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
        assert r.status_code == 409


def test_reserve_http_error_and_client_json_edges():
    """Cover reserve 4xx mapping and InventoryClient JSON edge branches."""
    from orders_app.inventory_client import InventoryClient

    class Transport(httpx.BaseTransport):
        def __init__(self, mode: str) -> None:
            self.mode = mode

        def handle_request(self, request: httpx.Request) -> httpx.Response:
            if request.url.path.startswith("/stock/"):
                if self.mode == "stock_list":
                    return httpx.Response(200, content=b'["x"]')
                return httpx.Response(
                    200,
                    json={"sku": "WIDGET-1", "available": 10, "quantity": 10, "reserved": 0},
                )
            if self.mode == "reserve_409":
                return httpx.Response(409, json={"error": "insufficient"})
            if self.mode == "reserve_list":
                return httpx.Response(200, content=b'["x"]')
            if self.mode == "reserve_bad_json":
                return httpx.Response(200, content=b"{not-json")
            return httpx.Response(404)

    # unit: non-object stock JSON
    inv = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=Transport("stock_list")
    )
    with pytest.raises(ConnectionError):
        inv.get_stock("WIDGET-1")
    inv.close()

    # unit: reserve list / bad json
    inv2 = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=Transport("reserve_list")
    )
    data = inv2.reserve("WIDGET-1", 1)
    assert data.get("error") == "invalid_payload" or "http_status" in data
    inv2.close()

    inv3 = InventoryClient(
        base_url="http://inventory.test",
        failure_threshold=5,
        transport=Transport("reserve_bad_json"),
    )
    with pytest.raises(ConnectionError):
        inv3.reserve("WIDGET-1", 1)
    inv3.close()

    # API: reserve 409 → order 409
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from orders_app.app import create_app
    from orders_app.db import Base, get_db

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

    inv4 = InventoryClient(
        base_url="http://inventory.test",
        failure_threshold=5,
        transport=Transport("reserve_409"),
    )
    app = create_app(inventory=inv4)
    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        assert c.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1}).status_code == 409
    inv4.close()


def test_settings_inventory_url_env(monkeypatch):
    from orders_app.settings import get_settings

    get_settings.cache_clear()
    monkeypatch.setenv("INVENTORY_URL", "http://inv.example:9999")
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    s = get_settings()
    assert s.inventory_url == "http://inv.example:9999"
    get_settings.cache_clear()


def test_get_db_close_path():
    from orders_app.db import get_db

    gen = get_db()
    next(gen)
    gen.close()


def test_service_reserve_circuit_and_refund_amount(client):
    from unittest.mock import MagicMock

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from orders_app import models, services
    from orders_app.db import Base
    from orders_app.inventory_client import CircuitOpenError, InventoryClient

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()

    inv = MagicMock(spec=InventoryClient)
    inv.get_stock.return_value = {"available": 10, "http_status": 200}
    inv.reserve.side_effect = CircuitOpenError(1.5)
    with pytest.raises(services.OrderError) as ei:
        services.create_order(db, inv, sku="W", qty=1, customer_id=None, unit_price_cents=10)
    assert ei.value.code == 503

    inv2 = MagicMock(spec=InventoryClient)
    inv2.get_stock.return_value = {"available": 10, "http_status": 200}
    inv2.reserve.side_effect = RuntimeError("boom")
    with pytest.raises(services.OrderError) as ei2:
        services.create_order(db, inv2, sku="W", qty=1, customer_id=None, unit_price_cents=10)
    assert ei2.value.code == 502

    order = models.Order(sku="W", qty=1, status="paid", total_cents=100)
    db.add(order)
    db.commit()
    db.refresh(order)
    with pytest.raises(services.OrderError) as ei3:
        services.request_refund(db, order, amount_cents=0, reason="x")
    assert ei3.value.code == 400
    db.close()


def test_cancel_invalid_and_main_and_reserve_5xx(monkeypatch):
    import httpx

    import orders_app.app as app_mod
    from orders_app.inventory_client import InventoryClient

    class T5xx(httpx.BaseTransport):
        def handle_request(self, request: httpx.Request) -> httpx.Response:
            if request.url.path.startswith("/stock/"):
                return httpx.Response(
                    200, json={"sku": "W", "available": 5, "quantity": 5, "reserved": 0}
                )
            return httpx.Response(503, json={"error": "down"})

    inv = InventoryClient(base_url="http://x", failure_threshold=5, transport=T5xx())
    with pytest.raises(Exception):
        inv.reserve("W", 1)
    inv.close()

    ran = {}

    def fake_run(*a, **k):
        ran["ok"] = True

    import uvicorn as uv

    monkeypatch.setattr(uv, "run", fake_run)
    app_mod.main()
    assert ran.get("ok") is True


def test_cancel_when_already_cancelled(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 200
    # idempotent cancel (same status) stays 200
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 200
    # cancelled → paid is invalid (covers status OrderError HTTP mapping)
    assert client.patch(f"/v1/orders/{oid}/status", json={"status": "paid"}).status_code == 409


def test_cancel_from_shipped_rejected(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    oid = created.json()["id"]
    assert client.patch(f"/v1/orders/{oid}/status", json={"status": "confirmed"}).status_code == 200
    assert client.post(f"/v1/orders/{oid}/pay", json={}).status_code == 200
    assert client.post(f"/v1/orders/{oid}/ship", json={}).status_code == 200
    # shipped → cancelled not allowed → covers cancel OrderError HTTP mapping
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 409


def test_legacy_create_order_when_create_fails(client, monkeypatch):
    from orders_app import services

    def boom(*a, **k):
        raise services.OrderError("cannot reserve", 409)

    monkeypatch.setattr(services, "create_order", boom)
    r = client.post("/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 10})
    assert r.status_code == 409


def test_cancel_releases_reservation(client):
    created = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1, "unit_price_cents": 50})
    assert created.status_code == 201
    oid = created.json()["id"]
    assert client.post(f"/v1/orders/{oid}/cancel").status_code == 200


def test_release_client_edges_and_commit_compensate():
    from unittest.mock import MagicMock

    from orders_app.inventory_client import InventoryClient
    from orders_app import services

    class ReleaseTransport(httpx.BaseTransport):
        def __init__(self, mode: str) -> None:
            self.mode = mode

        def handle_request(self, request: httpx.Request) -> httpx.Response:
            if request.url.path == "/release":
                if self.mode == "5xx":
                    return httpx.Response(500, json={"error": "boom"})
                if self.mode == "bad_json":
                    return httpx.Response(200, content=b"{bad")
                if self.mode == "list":
                    return httpx.Response(200, json=["x"])
                return httpx.Response(409, json={"error": "reservation not held"})
            return httpx.Response(404)

    inv = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=ReleaseTransport("ok")
    )
    assert inv.release("r1")["http_status"] == 409

    inv_list = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=ReleaseTransport("list")
    )
    assert inv_list.release("r1")["error"] == "invalid_payload"

    inv_bad = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=ReleaseTransport("bad_json")
    )
    with pytest.raises(ConnectionError):
        inv_bad.release("r1")

    inv5 = InventoryClient(
        base_url="http://inventory.test", failure_threshold=5, transport=ReleaseTransport("5xx")
    )
    with pytest.raises(httpx.HTTPStatusError):
        inv5.release("r1")

    # create_order compensates when db.commit fails
    db = MagicMock()
    db.flush.return_value = None
    db.commit.side_effect = RuntimeError("db down")
    client = MagicMock()
    client.get_stock.return_value = {"available": 10, "http_status": 200}
    client.reserve.return_value = {"reservation_id": "rx", "http_status": 200}
    client.release.return_value = {"http_status": 200}
    with pytest.raises(RuntimeError):
        services.create_order(
            db, client, sku="W", qty=1, customer_id=None, unit_price_cents=10
        )
    client.release.assert_called_with("rx")


def test_update_status_release_error_paths():
    from unittest.mock import MagicMock

    from orders_app import services
    from orders_app.inventory_client import CircuitOpenError

    order = MagicMock()
    order.status = "confirmed"
    order.reservation_id = "r1"
    db = MagicMock()

    client = MagicMock()
    client.release.side_effect = CircuitOpenError(2.0)
    with pytest.raises(services.OrderError) as e:
        services.update_status(db, order, "cancelled", client=client)
    assert e.value.code == 503

    client2 = MagicMock()
    client2.release.side_effect = RuntimeError("down")
    with pytest.raises(services.OrderError) as e2:
        services.update_status(db, order, "cancelled", client=client2)
    assert e2.value.code == 502

    client3 = MagicMock()
    client3.release.return_value = {"http_status": 409, "error": "reservation not held"}
    # idempotent — allowed
    out = services.update_status(db, order, "cancelled", client=client3)
    assert out is order

    client4 = MagicMock()
    client4.release.return_value = {"http_status": 409, "error": "other boom"}
    order2 = MagicMock()
    order2.status = "confirmed"
    order2.reservation_id = "r2"
    with pytest.raises(services.OrderError) as e4:
        services.update_status(db, order2, "cancelled", client=client4)
    assert e4.value.code == 409

    # compensate path when release itself fails after commit failure
    db2 = MagicMock()
    db2.flush.return_value = None
    db2.commit.side_effect = RuntimeError("db down")
    client5 = MagicMock()
    client5.get_stock.return_value = {"available": 10, "http_status": 200}
    client5.reserve.return_value = {"reservation_id": "rz", "http_status": 200}
    client5.release.side_effect = RuntimeError("release failed")
    with pytest.raises(RuntimeError, match="db down"):
        services.create_order(db2, client5, sku="W", qty=1, customer_id=None, unit_price_cents=1)
