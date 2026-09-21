"""Orders API + circuit-breaker edge cases (mocked inventory)."""

from __future__ import annotations

import httpx

from orders_app.app import create_app
from orders_app.inventory_client import InventoryClient


class _MockTransport(httpx.BaseTransport):
    def __init__(self, handler):
        self.handler = handler
        self.calls = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.calls += 1
        return self.handler(request)


def _app_with(handler):
    transport = _MockTransport(handler)
    inv = InventoryClient(
        base_url="http://inventory.test",
        failure_threshold=2,
        recovery_timeout=60,
        transport=transport,
    )
    app = create_app(inventory=inv)
    app.config["TESTING"] = True
    return app.test_client(), inv, transport


def test_health_reports_circuit() -> None:
    client, _, _ = _app_with(
        lambda req: httpx.Response(200, json={"sku": "x", "available": 1})
    )
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["circuit"]["state"] == "closed"


def test_create_order_ok() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path.startswith("/stock/"):
            return httpx.Response(
                200, json={"sku": "sku-100", "available": 50, "quantity": 50, "reserved": 0}
            )
        return httpx.Response(
            200, json={"sku": "sku-100", "status": "reserved", "available": 49, "reserved": 1}
        )

    client, _, _ = _app_with(handler)
    r = client.post("/orders", json={"sku": "sku-100", "qty": 1})
    assert r.status_code == 201
    body = r.get_json()
    assert body["status"] == "confirmed"
    oid = body["order_id"]
    assert client.get(f"/orders/{oid}").status_code == 200


def test_insufficient_stock() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"sku": "sku-200", "available": 0, "quantity": 0, "reserved": 0}
        )

    client, _, _ = _app_with(handler)
    r = client.post("/orders", json={"sku": "sku-200", "qty": 1})
    assert r.status_code == 409


def test_unknown_sku() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "unknown"})

    client, _, _ = _app_with(handler)
    r = client.post("/orders", json={"sku": "missing", "qty": 1})
    assert r.status_code == 404


def test_bad_payload() -> None:
    client, _, _ = _app_with(lambda req: httpx.Response(200, json={}))
    assert client.post("/orders", json={"sku": "", "qty": 0}).status_code == 400


def test_circuit_opens_on_repeated_5xx() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="down")

    client, inv, transport = _app_with(handler)
    r1 = client.post("/orders", json={"sku": "sku-100", "qty": 1})
    r2 = client.post("/orders", json={"sku": "sku-100", "qty": 1})
    assert r1.status_code == 502
    assert r2.status_code == 502
    # third call should short-circuit (circuit open) → 503 inventory_unavailable
    r3 = client.post("/orders", json={"sku": "sku-100", "qty": 1})
    assert r3.status_code == 503
    assert r3.get_json()["circuit"] == "open"
    assert inv.breaker.stats().state.value == "open"
    # no further downstream calls while open
    calls_after_open = transport.calls
    client.post("/orders", json={"sku": "sku-100", "qty": 1})
    assert transport.calls == calls_after_open


def test_order_not_found() -> None:
    client, _, _ = _app_with(lambda req: httpx.Response(200, json={}))
    assert client.get("/orders/nope").status_code == 404
