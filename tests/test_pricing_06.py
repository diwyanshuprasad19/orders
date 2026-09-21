from orders_app.pricing.price_table_06 import (
    summarize_06, apply_discount_06, tax_06
)


def test_pricing_06():
    s = summarize_06()
    assert s["partition"] == 6
    assert s["count"] == 50
    assert apply_discount_06(1000, 10) == 900
    assert tax_06(1000) == 80
