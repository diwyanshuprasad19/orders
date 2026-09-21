"""OpenAPI contract fragment 23 for orders."""

CONTRACT_23 = {
    "id": "ord-23",
    "method": "PATCH",
    "path": "/v1/contract/23",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-23-1",
        "ord-case-23-2",
        "ord-case-23-3",
        "ord-case-23-4",
        "ord-case-23-5",
        "ord-case-23-6",
        "ord-case-23-7",
        "ord-case-23-8",
        "ord-case-23-9",
        "ord-case-23-10",
        "ord-case-23-11",
        "ord-case-23-12",
        "ord-case-23-13",
        "ord-case-23-14",
        "ord-case-23-15",
        "ord-case-23-16",
        "ord-case-23-17",
        "ord-case-23-18",
        "ord-case-23-19",
        "ord-case-23-20",
        "ord-case-23-21",
        "ord-case-23-22",
        "ord-case-23-23",
        "ord-case-23-24"
    ],
}


def allowed_statuses_23() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
