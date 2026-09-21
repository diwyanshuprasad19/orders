"""OpenAPI contract fragment 22 for orders."""

CONTRACT_22 = {
    "id": "ord-22",
    "method": "POST",
    "path": "/v1/contract/22",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-22-1",
        "ord-case-22-2",
        "ord-case-22-3",
        "ord-case-22-4",
        "ord-case-22-5",
        "ord-case-22-6",
        "ord-case-22-7",
        "ord-case-22-8",
        "ord-case-22-9",
        "ord-case-22-10",
        "ord-case-22-11",
        "ord-case-22-12",
        "ord-case-22-13",
        "ord-case-22-14",
        "ord-case-22-15",
        "ord-case-22-16",
        "ord-case-22-17",
        "ord-case-22-18",
        "ord-case-22-19",
        "ord-case-22-20",
        "ord-case-22-21",
        "ord-case-22-22",
        "ord-case-22-23",
        "ord-case-22-24",
    ],
}


def allowed_statuses_22() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
