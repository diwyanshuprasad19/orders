from orders_app.pricing.price_table_12 import (
    summarize_12, apply_discount_12, tax_12
)


def test_pricing_12():
    s = summarize_12()
    assert s["partition"] == 12
    assert s["count"] == 50
    assert apply_discount_12(1000, 10) == 900
    assert tax_12(1000) == 80
