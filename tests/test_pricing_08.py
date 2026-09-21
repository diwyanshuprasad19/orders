from orders_app.pricing.price_table_08 import apply_discount_08, summarize_08, tax_08


def test_pricing_08():
    s = summarize_08()
    assert s["partition"] == 8
    assert s["count"] == 50
    assert apply_discount_08(1000, 10) == 900
    assert tax_08(1000) == 80
