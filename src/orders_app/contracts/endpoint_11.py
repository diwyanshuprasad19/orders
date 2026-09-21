"""OpenAPI contract fragment 11 for orders."""

CONTRACT_11 = {
    "id": "ord-11",
    "method": "PATCH",
    "path": "/v1/contract/11",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-11-1",
        "ord-case-11-2",
        "ord-case-11-3",
        "ord-case-11-4",
        "ord-case-11-5",
        "ord-case-11-6",
        "ord-case-11-7",
        "ord-case-11-8",
        "ord-case-11-9",
        "ord-case-11-10",
        "ord-case-11-11",
        "ord-case-11-12",
        "ord-case-11-13",
        "ord-case-11-14",
        "ord-case-11-15",
        "ord-case-11-16",
        "ord-case-11-17",
        "ord-case-11-18",
        "ord-case-11-19",
        "ord-case-11-20",
        "ord-case-11-21",
        "ord-case-11-22",
        "ord-case-11-23",
        "ord-case-11-24"
    ],
}


def allowed_statuses_11() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
