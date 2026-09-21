"""Pricing table partition 08."""

from __future__ import annotations

PRICES_08: dict[str, int] = {
    f"SKU-08-{j:03d}": 100 * 8 + j * 17
    for j in range(1, 51)
}


def price_of_08(sku: str) -> int | None:
    return PRICES_08.get(sku)


def apply_discount_08(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_08(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_08() -> dict:
    vals = list(PRICES_08.values())
    return {
        "partition": 8,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
