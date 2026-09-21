"""Pricing table partition 21."""

from __future__ import annotations

PRICES_21: dict[str, int] = {
    f"SKU-21-{j:03d}": 100 * 21 + j * 17
    for j in range(1, 51)
}


def price_of_21(sku: str) -> int | None:
    return PRICES_21.get(sku)


def apply_discount_21(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_21(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_21() -> dict:
    vals = list(PRICES_21.values())
    return {
        "partition": 21,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
