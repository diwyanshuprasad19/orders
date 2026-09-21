from orders_app.pricing.price_table_15 import apply_discount_15, summarize_15, tax_15


def test_pricing_15():
    s = summarize_15()
    assert s["partition"] == 15
    assert s["count"] == 50
    assert apply_discount_15(1000, 10) == 900
    assert tax_15(1000) == 80
