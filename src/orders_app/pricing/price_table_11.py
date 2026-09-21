"""Pricing table partition 11."""

from __future__ import annotations

PRICES_11: dict[str, int] = {f"SKU-11-{j:03d}": 100 * 11 + j * 17 for j in range(1, 51)}


def price_of_11(sku: str) -> int | None:
    return PRICES_11.get(sku)


def apply_discount_11(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_11(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_11() -> dict:
    vals = list(PRICES_11.values())
    return {
        "partition": 11,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
