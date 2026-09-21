"""Pricing table partition 17."""

from __future__ import annotations

PRICES_17: dict[str, int] = {f"SKU-17-{j:03d}": 100 * 17 + j * 17 for j in range(1, 51)}


def price_of_17(sku: str) -> int | None:
    return PRICES_17.get(sku)


def apply_discount_17(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_17(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_17() -> dict:
    vals = list(PRICES_17.values())
    return {
        "partition": 17,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
