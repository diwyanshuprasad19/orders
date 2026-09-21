from orders_app.pricing.price_table_04 import (
    summarize_04, apply_discount_04, tax_04
)


def test_pricing_04():
    s = summarize_04()
    assert s["partition"] == 4
    assert s["count"] == 50
    assert apply_discount_04(1000, 10) == 900
    assert tax_04(1000) == 80
