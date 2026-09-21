"""Pricing table partition 04."""

from __future__ import annotations

PRICES_04: dict[str, int] = {f"SKU-04-{j:03d}": 100 * 4 + j * 17 for j in range(1, 51)}


def price_of_04(sku: str) -> int | None:
    return PRICES_04.get(sku)


def apply_discount_04(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_04(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_04() -> dict:
    vals = list(PRICES_04.values())
    return {
        "partition": 4,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
