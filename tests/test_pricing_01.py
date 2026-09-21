from orders_app.pricing.price_table_01 import (
    summarize_01, apply_discount_01, tax_01
)


def test_pricing_01():
    s = summarize_01()
    assert s["partition"] == 1
    assert s["count"] == 50
    assert apply_discount_01(1000, 10) == 900
    assert tax_01(1000) == 80
