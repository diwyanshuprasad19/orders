"""OpenAPI contract fragment 15 for orders."""

CONTRACT_15 = {
    "id": "ord-15",
    "method": "GET",
    "path": "/v1/contract/15",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-15-1",
        "ord-case-15-2",
        "ord-case-15-3",
        "ord-case-15-4",
        "ord-case-15-5",
        "ord-case-15-6",
        "ord-case-15-7",
        "ord-case-15-8",
        "ord-case-15-9",
        "ord-case-15-10",
        "ord-case-15-11",
        "ord-case-15-12",
        "ord-case-15-13",
        "ord-case-15-14",
        "ord-case-15-15",
        "ord-case-15-16",
        "ord-case-15-17",
        "ord-case-15-18",
        "ord-case-15-19",
        "ord-case-15-20",
        "ord-case-15-21",
        "ord-case-15-22",
        "ord-case-15-23",
        "ord-case-15-24"
    ],
}


def allowed_statuses_15() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
