"""Pricing table partition 05."""

from __future__ import annotations

PRICES_05: dict[str, int] = {f"SKU-05-{j:03d}": 100 * 5 + j * 17 for j in range(1, 51)}


def price_of_05(sku: str) -> int | None:
    return PRICES_05.get(sku)


def apply_discount_05(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_05(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_05() -> dict:
    vals = list(PRICES_05.values())
    return {
        "partition": 5,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
