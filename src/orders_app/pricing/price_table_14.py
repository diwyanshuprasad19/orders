"""Pricing table partition 14."""

from __future__ import annotations

PRICES_14: dict[str, int] = {f"SKU-14-{j:03d}": 100 * 14 + j * 17 for j in range(1, 51)}


def price_of_14(sku: str) -> int | None:
    return PRICES_14.get(sku)


def apply_discount_14(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_14(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_14() -> dict:
    vals = list(PRICES_14.values())
    return {
        "partition": 14,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
