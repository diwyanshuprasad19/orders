"""Pricing table partition 27."""

from __future__ import annotations

PRICES_27: dict[str, int] = {
    f"SKU-27-{j:03d}": 100 * 27 + j * 17
    for j in range(1, 51)
}


def price_of_27(sku: str) -> int | None:
    return PRICES_27.get(sku)


def apply_discount_27(cents: int, pct: float) -> int:
    pct = max(0.0, min(90.0, pct))
    return int(cents * (1.0 - pct / 100.0))


def tax_27(cents: int, rate: float = 0.08) -> int:
    return int(cents * rate)


def summarize_27() -> dict:
    vals = list(PRICES_27.values())
    return {
        "partition": 27,
        "count": len(vals),
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) // len(vals),
    }
