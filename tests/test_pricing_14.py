from orders_app.pricing.price_table_14 import (
    summarize_14, apply_discount_14, tax_14
)


def test_pricing_14():
    s = summarize_14()
    assert s["partition"] == 14
    assert s["count"] == 50
    assert apply_discount_14(1000, 10) == 900
    assert tax_14(1000) == 80
