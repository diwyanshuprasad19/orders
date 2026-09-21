"""Pricing table partition 28."""

from __future__ import annotations

PRICES_28: dict[str, int] = {
    f"SKU-28-{j:03d}": 100 * 28 + j * 17
    for j in range(1, 51)
}


def price_of_28(sku: str) -> int | None:
    return PRICES_28.get(sku)


def apply_discount_28(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_28(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_28() -> dict:
    vals = list(PRICES_28.values())
    return {
        "partition": 28,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
