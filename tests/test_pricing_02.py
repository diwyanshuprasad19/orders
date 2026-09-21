from orders_app.pricing.price_table_02 import apply_discount_02, summarize_02, tax_02


def test_pricing_02():
    s = summarize_02()
    assert s["partition"] == 2
    assert s["count"] == 50
    assert apply_discount_02(1000, 10) == 900
    assert tax_02(1000) == 80
