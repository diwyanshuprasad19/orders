"""Pricing table partition 09."""

from __future__ import annotations

PRICES_09: dict[str, int] = {f"SKU-09-{j:03d}": 100 * 9 + j * 17 for j in range(1, 51)}


def price_of_09(sku: str) -> int | None:
    return PRICES_09.get(sku)


def apply_discount_09(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_09(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_09() -> dict:
    vals = list(PRICES_09.values())
    return {
        "partition": 9,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
