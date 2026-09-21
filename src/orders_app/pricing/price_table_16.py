"""Pricing table partition 16."""

from __future__ import annotations

PRICES_16: dict[str, int] = {
    f"SKU-16-{j:03d}": 100 * 16 + j * 17
    for j in range(1, 51)
}


def price_of_16(sku: str) -> int | None:
    return PRICES_16.get(sku)


def apply_discount_16(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_16(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_16() -> dict:
    vals = list(PRICES_16.values())
    return {
        "partition": 16,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
