"""Pricing table partition 24."""

from __future__ import annotations

PRICES_24: dict[str, int] = {
    f"SKU-24-{j:03d}": 100 * 24 + j * 17
    for j in range(1, 51)
}


def price_of_24(sku: str) -> int | None:
    return PRICES_24.get(sku)


def apply_discount_24(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_24(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_24() -> dict:
    vals = list(PRICES_24.values())
    return {
        "partition": 24,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
