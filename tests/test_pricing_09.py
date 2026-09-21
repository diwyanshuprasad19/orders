from orders_app.pricing.price_table_09 import (
    summarize_09, apply_discount_09, tax_09
)


def test_pricing_09():
    s = summarize_09()
    assert s["partition"] == 9
    assert s["count"] == 50
    assert apply_discount_09(1000, 10) == 900
    assert tax_09(1000) == 80
