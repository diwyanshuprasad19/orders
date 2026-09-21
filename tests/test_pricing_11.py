from orders_app.pricing.price_table_11 import (
    summarize_11, apply_discount_11, tax_11
)


def test_pricing_11():
    s = summarize_11()
    assert s["partition"] == 11
    assert s["count"] == 50
    assert apply_discount_11(1000, 10) == 900
    assert tax_11(1000) == 80
