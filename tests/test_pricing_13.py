from orders_app.pricing.price_table_13 import apply_discount_13, summarize_13, tax_13


def test_pricing_13():
    s = summarize_13()
    assert s["partition"] == 13
    assert s["count"] == 50
    assert apply_discount_13(1000, 10) == 900
    assert tax_13(1000) == 80
