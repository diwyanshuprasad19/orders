"""OpenAPI contract fragment 18 for orders."""

CONTRACT_18 = {
    "id": "ord-18",
    "method": "GET",
    "path": "/v1/contract/18",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-18-1",
        "ord-case-18-2",
        "ord-case-18-3",
        "ord-case-18-4",
        "ord-case-18-5",
        "ord-case-18-6",
        "ord-case-18-7",
        "ord-case-18-8",
        "ord-case-18-9",
        "ord-case-18-10",
        "ord-case-18-11",
        "ord-case-18-12",
        "ord-case-18-13",
        "ord-case-18-14",
        "ord-case-18-15",
        "ord-case-18-16",
        "ord-case-18-17",
        "ord-case-18-18",
        "ord-case-18-19",
        "ord-case-18-20",
        "ord-case-18-21",
        "ord-case-18-22",
        "ord-case-18-23",
        "ord-case-18-24"
    ],
}


def allowed_statuses_18() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
