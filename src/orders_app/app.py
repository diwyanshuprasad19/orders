"""Orders HTTP API — creates orders only when inventory allows (via circuit breaker)."""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

import httpx
from flask import Flask, jsonify, request

_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from orders_app.inventory_client import CircuitOpenError, InventoryClient

try:
    from distributed_tracing import configure_tracing, get_tracer
except ImportError:  # pragma: no cover
    configure_tracing = None  # type: ignore
    get_tracer = None  # type: ignore


def create_app(inventory: InventoryClient | None = None) -> Flask:
    app = Flask(__name__)
    if configure_tracing:
        configure_tracing(os.getenv("OTEL_SERVICE_NAME", "orders"))
    client = inventory or InventoryClient()
    app.extensions["inventory"] = client
    orders: dict[str, dict] = {}

    @app.get("/health")
    def health():
        stats = client.breaker.stats()
        return jsonify(
            {
                "status": "ok",
                "service": "orders",
                "circuit": {
                    "state": stats.state.value,
                    "failures": stats.failures,
                },
            }
        )

    @app.post("/orders")
    def create_order():
        data = request.get_json(silent=True) or {}
        sku = str(data.get("sku", "")).strip()
        qty = int(data.get("qty", 0))
        if not sku or qty <= 0:
            return jsonify({"error": "sku and qty>0 required"}), 400

        tracer = get_tracer(__name__) if get_tracer else None
        span_cm = tracer.start_as_current_span("orders.create") if tracer else None
        try:
            if span_cm:
                span_cm.__enter__()
            try:
                stock = client.get_stock(sku)
            except CircuitOpenError as exc:
                return (
                    jsonify(
                        {
                            "error": "inventory_unavailable",
                            "circuit": "open",
                            "retry_after": exc.retry_after,
                        }
                    ),
                    503,
                )
            except (ConnectionError, httpx.HTTPError) as exc:
                return jsonify({"error": "inventory_error", "detail": str(exc)}), 502

            if stock.get("error") == "not_found":
                return jsonify({"error": "unknown_sku", "sku": sku}), 404
            if int(stock.get("available", 0)) < qty:
                return (
                    jsonify(
                        {
                            "error": "insufficient_stock",
                            "available": stock.get("available", 0),
                        }
                    ),
                    409,
                )

            try:
                reserved = client.reserve(sku, qty)
            except CircuitOpenError as exc:
                return (
                    jsonify(
                        {
                            "error": "inventory_unavailable",
                            "circuit": "open",
                            "retry_after": exc.retry_after,
                        }
                    ),
                    503,
                )
            except (ConnectionError, httpx.HTTPError) as exc:
                return jsonify({"error": "inventory_error", "detail": str(exc)}), 502

            if reserved.get("http_status", 200) >= 400:
                return jsonify(reserved), int(reserved.get("http_status", 409))

            order_id = str(uuid.uuid4())
            order = {"order_id": order_id, "sku": sku, "qty": qty, "status": "confirmed"}
            orders[order_id] = order
            return jsonify(order), 201
        finally:
            if span_cm:
                span_cm.__exit__(None, None, None)

    @app.get("/orders/<order_id>")
    def get_order(order_id: str):
        order = orders.get(order_id)
        if not order:
            return jsonify({"error": "not_found"}), 404
        return jsonify(order)

    return app


app = create_app()


def main() -> None:
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8092")), debug=False)


if __name__ == "__main__":
    main()
