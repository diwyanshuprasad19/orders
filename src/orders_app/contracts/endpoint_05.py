"""OpenAPI contract fragment 05 for orders."""

CONTRACT_05 = {
    "id": "ord-05",
    "method": "PATCH",
    "path": "/v1/contract/05",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-5-1",
        "ord-case-5-2",
        "ord-case-5-3",
        "ord-case-5-4",
        "ord-case-5-5",
        "ord-case-5-6",
        "ord-case-5-7",
        "ord-case-5-8",
        "ord-case-5-9",
        "ord-case-5-10",
        "ord-case-5-11",
        "ord-case-5-12",
        "ord-case-5-13",
        "ord-case-5-14",
        "ord-case-5-15",
        "ord-case-5-16",
        "ord-case-5-17",
        "ord-case-5-18",
        "ord-case-5-19",
        "ord-case-5-20",
        "ord-case-5-21",
        "ord-case-5-22",
        "ord-case-5-23",
        "ord-case-5-24",
    ],
}


def allowed_statuses_05() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
