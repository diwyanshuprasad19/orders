"""Pricing table partition 20."""

from __future__ import annotations

PRICES_20: dict[str, int] = {
    f"SKU-20-{j:03d}": 100 * 20 + j * 17
    for j in range(1, 51)
}


def price_of_20(sku: str) -> int | None:
    return PRICES_20.get(sku)


def apply_discount_20(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_20(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_20() -> dict:
    vals = list(PRICES_20.values())
    return {
        "partition": 20,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
