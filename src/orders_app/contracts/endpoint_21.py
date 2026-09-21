"""OpenAPI contract fragment 21 for orders."""

CONTRACT_21 = {
    "id": "ord-21",
    "method": "GET",
    "path": "/v1/contract/21",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-21-1",
        "ord-case-21-2",
        "ord-case-21-3",
        "ord-case-21-4",
        "ord-case-21-5",
        "ord-case-21-6",
        "ord-case-21-7",
        "ord-case-21-8",
        "ord-case-21-9",
        "ord-case-21-10",
        "ord-case-21-11",
        "ord-case-21-12",
        "ord-case-21-13",
        "ord-case-21-14",
        "ord-case-21-15",
        "ord-case-21-16",
        "ord-case-21-17",
        "ord-case-21-18",
        "ord-case-21-19",
        "ord-case-21-20",
        "ord-case-21-21",
        "ord-case-21-22",
        "ord-case-21-23",
        "ord-case-21-24"
    ],
}


def allowed_statuses_21() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
