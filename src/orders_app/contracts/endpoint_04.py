"""OpenAPI contract fragment 04 for orders."""

CONTRACT_04 = {
    "id": "ord-04",
    "method": "POST",
    "path": "/v1/contract/04",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-4-1",
        "ord-case-4-2",
        "ord-case-4-3",
        "ord-case-4-4",
        "ord-case-4-5",
        "ord-case-4-6",
        "ord-case-4-7",
        "ord-case-4-8",
        "ord-case-4-9",
        "ord-case-4-10",
        "ord-case-4-11",
        "ord-case-4-12",
        "ord-case-4-13",
        "ord-case-4-14",
        "ord-case-4-15",
        "ord-case-4-16",
        "ord-case-4-17",
        "ord-case-4-18",
        "ord-case-4-19",
        "ord-case-4-20",
        "ord-case-4-21",
        "ord-case-4-22",
        "ord-case-4-23",
        "ord-case-4-24",
    ],
}


def allowed_statuses_04() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
