from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import httpx

_DT = Path(__file__).resolve().parents[3] / "distributed-tracing" / "src"
if _DT.is_dir():
    sys.path.insert(0, str(_DT))

from distributed_tracing import CircuitBreaker, CircuitOpenError, inject_context

from orders_app.settings import get_settings

# re-export for app
__all__ = ["InventoryClient", "CircuitOpenError"]


class InventoryClient:
    def __init__(
        self,
        base_url: str | None = None,
        *,
        failure_threshold: int | None = None,
        recovery_timeout: float | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        s = get_settings()
        self.base_url = (base_url or s.inventory_url).rstrip("/")
        self.breaker: CircuitBreaker = CircuitBreaker(
            failure_threshold=failure_threshold or s.cb_failure_threshold,
            recovery_timeout=recovery_timeout or s.cb_recovery_timeout,
            name="inventory",
        )
        self._client = httpx.Client(timeout=5.0, transport=transport)

    def _headers(self) -> dict[str, str]:
        h = {"accept": "application/json"}
        inject_context(h)
        return h

    def get_stock(self, sku: str) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            r = self._client.get(f"{self.base_url}/stock/{sku}", headers=self._headers())
            if r.status_code == 404:
                return {"error": "not_found", "sku": sku, "http_status": 404}
            r.raise_for_status()
            try:
                data = r.json()
            except ValueError as exc:
                raise ConnectionError(f"inventory returned invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                raise ConnectionError("inventory returned non-object JSON")
            data["http_status"] = r.status_code
            return data

        return self.breaker.call(_call)

    def reserve(self, sku: str, qty: int) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            r = self._client.post(
                f"{self.base_url}/reserve",
                json={"sku": sku, "qty": qty},
                headers=self._headers(),
            )
            if r.status_code >= 500:
                r.raise_for_status()
            try:
                data = r.json() if r.content else {}
            except ValueError as exc:
                raise ConnectionError(f"inventory returned invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                data = {"error": "invalid_payload", "raw": str(data)}
            data["http_status"] = r.status_code
            return data

        return self.breaker.call(_call)

    def release(self, reservation_id: str) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            r = self._client.post(
                f"{self.base_url}/release",
                json={"reservation_id": reservation_id},
                headers=self._headers(),
            )
            if r.status_code >= 500:
                r.raise_for_status()
            try:
                data = r.json() if r.content else {}
            except ValueError as exc:
                raise ConnectionError(f"inventory returned invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                data = {"error": "invalid_payload", "raw": str(data)}
            data["http_status"] = r.status_code
            return data

        return self.breaker.call(_call)

    def consume(self, reservation_id: str) -> dict[str, Any]:
        def _call() -> dict[str, Any]:
            r = self._client.post(
                f"{self.base_url}/consume",
                json={"reservation_id": reservation_id},
                headers=self._headers(),
            )
            if r.status_code >= 500:
                r.raise_for_status()
            try:
                data = r.json() if r.content else {}
            except ValueError as exc:
                raise ConnectionError(f"inventory returned invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                data = {"error": "invalid_payload", "raw": str(data)}
            data["http_status"] = r.status_code
            return data

        return self.breaker.call(_call)

    def close(self) -> None:
        self._client.close()
