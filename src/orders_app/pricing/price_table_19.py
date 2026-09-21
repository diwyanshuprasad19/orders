"""Pricing table partition 19."""

from __future__ import annotations

PRICES_19: dict[str, int] = {
    f"SKU-19-{j:03d}": 100 * 19 + j * 17
    for j in range(1, 51)
}


def price_of_19(sku: str) -> int | None:
    return PRICES_19.get(sku)


def apply_discount_19(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_19(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_19() -> dict:
    vals = list(PRICES_19.values())
    return {
        "partition": 19,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
