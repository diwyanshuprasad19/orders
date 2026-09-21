"""Pricing table partition 22."""

from __future__ import annotations

PRICES_22: dict[str, int] = {
    f"SKU-22-{j:03d}": 100 * 22 + j * 17
    for j in range(1, 51)
}


def price_of_22(sku: str) -> int | None:
    return PRICES_22.get(sku)


def apply_discount_22(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_22(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_22() -> dict:
    vals = list(PRICES_22.values())
    return {
        "partition": 22,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
