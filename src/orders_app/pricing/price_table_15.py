"""Pricing table partition 15."""

from __future__ import annotations

PRICES_15: dict[str, int] = {f"SKU-15-{j:03d}": 100 * 15 + j * 17 for j in range(1, 51)}


def price_of_15(sku: str) -> int | None:
    return PRICES_15.get(sku)


def apply_discount_15(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_15(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_15() -> dict:
    vals = list(PRICES_15.values())
    return {
        "partition": 15,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
