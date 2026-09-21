"""Pricing table partition 13."""

from __future__ import annotations

PRICES_13: dict[str, int] = {f"SKU-13-{j:03d}": 100 * 13 + j * 17 for j in range(1, 51)}


def price_of_13(sku: str) -> int | None:
    return PRICES_13.get(sku)


def apply_discount_13(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_13(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_13() -> dict:
    vals = list(PRICES_13.values())
    return {
        "partition": 13,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
