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
    def __init__(self):
        self.fail = False
        self.calls = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.calls += 1
        if self.fail:
            return httpx.Response(503, json={"error": "down"})
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


def test_circuit_opens(client):
    client.transport_fake.fail = True  # type: ignore

    # force failures through breaker (httpx raises on 503 via raise_for_status in get_stock path for 5xx)
    # Our fake returns 503 without raise in get_stock for stock path - adjust: get_stock only raises on raise_for_status for non-404
    # Make transport raise
    def boom(request):
        raise httpx.ConnectError("down")

    client.transport_fake.handle_request = boom  # type: ignore
    for _ in range(2):
        client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    r = client.post("/v1/orders", json={"sku": "WIDGET-1", "qty": 1})
    assert r.status_code == 503
    assert client.get("/v1/circuit").json()["state"] == "open"


def test_customers_seeded(client):
    assert len(client.get("/v1/customers").json()) >= 5
