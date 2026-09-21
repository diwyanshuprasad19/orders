"""OpenAPI contract fragment 01 for orders."""

CONTRACT_01 = {
    "id": "ord-01",
    "method": "POST",
    "path": "/v1/contract/01",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-1-1",
        "ord-case-1-2",
        "ord-case-1-3",
        "ord-case-1-4",
        "ord-case-1-5",
        "ord-case-1-6",
        "ord-case-1-7",
        "ord-case-1-8",
        "ord-case-1-9",
        "ord-case-1-10",
        "ord-case-1-11",
        "ord-case-1-12",
        "ord-case-1-13",
        "ord-case-1-14",
        "ord-case-1-15",
        "ord-case-1-16",
        "ord-case-1-17",
        "ord-case-1-18",
        "ord-case-1-19",
        "ord-case-1-20",
        "ord-case-1-21",
        "ord-case-1-22",
        "ord-case-1-23",
        "ord-case-1-24"
    ],
}


def allowed_statuses_01() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
