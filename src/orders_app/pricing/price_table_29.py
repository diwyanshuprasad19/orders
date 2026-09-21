"""Pricing table partition 29."""

from __future__ import annotations

PRICES_29: dict[str, int] = {f"SKU-29-{j:03d}": 100 * 29 + j * 17 for j in range(1, 51)}


def price_of_29(sku: str) -> int | None:
    return PRICES_29.get(sku)


def apply_discount_29(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_29(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_29() -> dict:
    vals = list(PRICES_29.values())
    return {
        "partition": 29,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
