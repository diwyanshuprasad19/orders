from orders_app.pricing.price_table_03 import apply_discount_03, summarize_03, tax_03


def test_pricing_03():
    s = summarize_03()
    assert s["partition"] == 3
    assert s["count"] == 50
    assert apply_discount_03(1000, 10) == 900
    assert tax_03(1000) == 80
