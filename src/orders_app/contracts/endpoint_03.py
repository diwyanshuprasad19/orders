"""OpenAPI contract fragment 03 for orders."""

CONTRACT_03 = {
    "id": "ord-03",
    "method": "GET",
    "path": "/v1/contract/03",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-3-1",
        "ord-case-3-2",
        "ord-case-3-3",
        "ord-case-3-4",
        "ord-case-3-5",
        "ord-case-3-6",
        "ord-case-3-7",
        "ord-case-3-8",
        "ord-case-3-9",
        "ord-case-3-10",
        "ord-case-3-11",
        "ord-case-3-12",
        "ord-case-3-13",
        "ord-case-3-14",
        "ord-case-3-15",
        "ord-case-3-16",
        "ord-case-3-17",
        "ord-case-3-18",
        "ord-case-3-19",
        "ord-case-3-20",
        "ord-case-3-21",
        "ord-case-3-22",
        "ord-case-3-23",
        "ord-case-3-24",
    ],
}


def allowed_statuses_03() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
