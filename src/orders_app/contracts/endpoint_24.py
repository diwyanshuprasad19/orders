"""OpenAPI contract fragment 24 for orders."""

CONTRACT_24 = {
    "id": "ord-24",
    "method": "GET",
    "path": "/v1/contract/24",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-24-1",
        "ord-case-24-2",
        "ord-case-24-3",
        "ord-case-24-4",
        "ord-case-24-5",
        "ord-case-24-6",
        "ord-case-24-7",
        "ord-case-24-8",
        "ord-case-24-9",
        "ord-case-24-10",
        "ord-case-24-11",
        "ord-case-24-12",
        "ord-case-24-13",
        "ord-case-24-14",
        "ord-case-24-15",
        "ord-case-24-16",
        "ord-case-24-17",
        "ord-case-24-18",
        "ord-case-24-19",
        "ord-case-24-20",
        "ord-case-24-21",
        "ord-case-24-22",
        "ord-case-24-23",
        "ord-case-24-24",
    ],
}


def allowed_statuses_24() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
