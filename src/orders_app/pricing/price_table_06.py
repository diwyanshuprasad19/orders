"""Pricing table partition 06."""

from __future__ import annotations

PRICES_06: dict[str, int] = {f"SKU-06-{j:03d}": 100 * 6 + j * 17 for j in range(1, 51)}


def price_of_06(sku: str) -> int | None:
    return PRICES_06.get(sku)


def apply_discount_06(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_06(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_06() -> dict:
    vals = list(PRICES_06.values())
    return {
        "partition": 6,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
