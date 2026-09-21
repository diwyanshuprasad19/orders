"""OpenAPI contract fragment 12 for orders."""

CONTRACT_12 = {
    "id": "ord-12",
    "method": "GET",
    "path": "/v1/contract/12",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-12-1",
        "ord-case-12-2",
        "ord-case-12-3",
        "ord-case-12-4",
        "ord-case-12-5",
        "ord-case-12-6",
        "ord-case-12-7",
        "ord-case-12-8",
        "ord-case-12-9",
        "ord-case-12-10",
        "ord-case-12-11",
        "ord-case-12-12",
        "ord-case-12-13",
        "ord-case-12-14",
        "ord-case-12-15",
        "ord-case-12-16",
        "ord-case-12-17",
        "ord-case-12-18",
        "ord-case-12-19",
        "ord-case-12-20",
        "ord-case-12-21",
        "ord-case-12-22",
        "ord-case-12-23",
        "ord-case-12-24",
    ],
}


def allowed_statuses_12() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
