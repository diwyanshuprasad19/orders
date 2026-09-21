"""OpenAPI contract fragment 07 for orders."""

CONTRACT_07 = {
    "id": "ord-07",
    "method": "POST",
    "path": "/v1/contract/07",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-7-1",
        "ord-case-7-2",
        "ord-case-7-3",
        "ord-case-7-4",
        "ord-case-7-5",
        "ord-case-7-6",
        "ord-case-7-7",
        "ord-case-7-8",
        "ord-case-7-9",
        "ord-case-7-10",
        "ord-case-7-11",
        "ord-case-7-12",
        "ord-case-7-13",
        "ord-case-7-14",
        "ord-case-7-15",
        "ord-case-7-16",
        "ord-case-7-17",
        "ord-case-7-18",
        "ord-case-7-19",
        "ord-case-7-20",
        "ord-case-7-21",
        "ord-case-7-22",
        "ord-case-7-23",
        "ord-case-7-24",
    ],
}


def allowed_statuses_07() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
