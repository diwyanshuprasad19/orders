"""Pricing table partition 01."""

from __future__ import annotations

PRICES_01: dict[str, int] = {f"SKU-01-{j:03d}": 100 * 1 + j * 17 for j in range(1, 51)}


def price_of_01(sku: str) -> int | None:
    return PRICES_01.get(sku)


def apply_discount_01(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_01(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_01() -> dict:
    vals = list(PRICES_01.values())
    return {
        "partition": 1,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
