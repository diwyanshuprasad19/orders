"""Pricing table partition 25."""

from __future__ import annotations

PRICES_25: dict[str, int] = {f"SKU-25-{j:03d}": 100 * 25 + j * 17 for j in range(1, 51)}


def price_of_25(sku: str) -> int | None:
    return PRICES_25.get(sku)


def apply_discount_25(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_25(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_25() -> dict:
    vals = list(PRICES_25.values())
    return {
        "partition": 25,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
