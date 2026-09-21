"""Pricing table partition 03."""

from __future__ import annotations

PRICES_03: dict[str, int] = {f"SKU-03-{j:03d}": 100 * 3 + j * 17 for j in range(1, 51)}


def price_of_03(sku: str) -> int | None:
    return PRICES_03.get(sku)


def apply_discount_03(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_03(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_03() -> dict:
    vals = list(PRICES_03.values())
    return {
        "partition": 3,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
