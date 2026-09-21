from orders_app.pricing.price_table_07 import apply_discount_07, summarize_07, tax_07


def test_pricing_07():
    s = summarize_07()
    assert s["partition"] == 7
    assert s["count"] == 50
    assert apply_discount_07(1000, 10) == 900
    assert tax_07(1000) == 80
