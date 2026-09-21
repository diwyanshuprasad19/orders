from orders_app.pricing.price_table_10 import (
    summarize_10, apply_discount_10, tax_10
)


def test_pricing_10():
    s = summarize_10()
    assert s["partition"] == 10
    assert s["count"] == 50
    assert apply_discount_10(1000, 10) == 900
    assert tax_10(1000) == 80
