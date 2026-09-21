"""Inventory HTTP client protected by circuit breaker + trace propagation."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import httpx

_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from distributed_tracing import CircuitBreaker, CircuitOpenError, inject_context


class InventoryClient:
    def __init__(
        self,
        base_url: str | None = None,
        *,
        timeout: float = 1.0,
        failure_threshold: int = 3,
        recovery_timeout: float = 5.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("INVENTORY_URL", "http://127.0.0.1:8091")).rstrip(
            "/"
        )
        self._client = httpx.Client(timeout=timeout, transport=transport)
        self.breaker = CircuitBreaker(
            "inventory",
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )

    def get_stock(self, sku: str) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            headers: dict[str, str] = {}
            inject_context(headers)
            resp = self._client.get(f"{self.base_url}/stock/{sku}", headers=headers)
            if resp.status_code >= 500:
                raise ConnectionError(f"inventory {resp.status_code}")
            if resp.status_code == 404:
                return {"error": "not_found", "sku": sku, "available": 0}
            resp.raise_for_status()
            return resp.json()

        return self.breaker.call(_call)

    def reserve(self, sku: str, qty: int) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            headers: dict[str, str] = {"content-type": "application/json"}
            inject_context(headers)
            resp = self._client.post(
                f"{self.base_url}/reserve",
                headers=headers,
                json={"sku": sku, "qty": qty},
            )
            if resp.status_code >= 500:
                raise ConnectionError(f"inventory {resp.status_code}")
            if resp.status_code >= 400:
                body = resp.json() if resp.headers.get("content-type", "").startswith(
                    "application/json"
                ) else {"error": resp.text}
                body["http_status"] = resp.status_code
                return body
            return resp.json()

        return self.breaker.call(_call)

    def close(self) -> None:
        self._client.close()


__all__ = ["CircuitOpenError", "InventoryClient"]
