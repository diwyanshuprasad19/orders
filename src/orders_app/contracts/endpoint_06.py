"""OpenAPI contract fragment 06 for orders."""

CONTRACT_06 = {
    "id": "ord-06",
    "method": "GET",
    "path": "/v1/contract/06",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-6-1",
        "ord-case-6-2",
        "ord-case-6-3",
        "ord-case-6-4",
        "ord-case-6-5",
        "ord-case-6-6",
        "ord-case-6-7",
        "ord-case-6-8",
        "ord-case-6-9",
        "ord-case-6-10",
        "ord-case-6-11",
        "ord-case-6-12",
        "ord-case-6-13",
        "ord-case-6-14",
        "ord-case-6-15",
        "ord-case-6-16",
        "ord-case-6-17",
        "ord-case-6-18",
        "ord-case-6-19",
        "ord-case-6-20",
        "ord-case-6-21",
        "ord-case-6-22",
        "ord-case-6-23",
        "ord-case-6-24"
    ],
}


def allowed_statuses_06() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
