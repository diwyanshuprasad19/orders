from orders_app.pricing.price_table_05 import apply_discount_05, summarize_05, tax_05


def test_pricing_05():
    s = summarize_05()
    assert s["partition"] == 5
    assert s["count"] == 50
    assert apply_discount_05(1000, 10) == 900
    assert tax_05(1000) == 80
