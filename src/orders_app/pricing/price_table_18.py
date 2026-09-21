"""Pricing table partition 18."""

from __future__ import annotations

PRICES_18: dict[str, int] = {f"SKU-18-{j:03d}": 100 * 18 + j * 17 for j in range(1, 51)}


def price_of_18(sku: str) -> int | None:
    return PRICES_18.get(sku)


def apply_discount_18(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_18(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_18() -> dict:
    vals = list(PRICES_18.values())
    return {
        "partition": 18,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
