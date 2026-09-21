"""Pricing table partition 12."""

from __future__ import annotations

PRICES_12: dict[str, int] = {
    f"SKU-12-{j:03d}": 100 * 12 + j * 17
    for j in range(1, 51)
}


def price_of_12(sku: str) -> int | None:
    return PRICES_12.get(sku)


def apply_discount_12(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_12(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_12() -> dict:
    vals = list(PRICES_12.values())
    return {
        "partition": 12,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
