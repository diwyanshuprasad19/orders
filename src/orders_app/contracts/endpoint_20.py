"""OpenAPI contract fragment 20 for orders."""

CONTRACT_20 = {
    "id": "ord-20",
    "method": "PATCH",
    "path": "/v1/contract/20",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-20-1",
        "ord-case-20-2",
        "ord-case-20-3",
        "ord-case-20-4",
        "ord-case-20-5",
        "ord-case-20-6",
        "ord-case-20-7",
        "ord-case-20-8",
        "ord-case-20-9",
        "ord-case-20-10",
        "ord-case-20-11",
        "ord-case-20-12",
        "ord-case-20-13",
        "ord-case-20-14",
        "ord-case-20-15",
        "ord-case-20-16",
        "ord-case-20-17",
        "ord-case-20-18",
        "ord-case-20-19",
        "ord-case-20-20",
        "ord-case-20-21",
        "ord-case-20-22",
        "ord-case-20-23",
        "ord-case-20-24"
    ],
}


def allowed_statuses_20() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
