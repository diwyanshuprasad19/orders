"""Pricing table partition 26."""

from __future__ import annotations

PRICES_26: dict[str, int] = {
    f"SKU-26-{j:03d}": 100 * 26 + j * 17
    for j in range(1, 51)
}


def price_of_26(sku: str) -> int | None:
    return PRICES_26.get(sku)


def apply_discount_26(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_26(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_26() -> dict:
    vals = list(PRICES_26.values())
    return {
        "partition": 26,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
