"""OpenAPI contract fragment 13 for orders."""

CONTRACT_13 = {
    "id": "ord-13",
    "method": "POST",
    "path": "/v1/contract/13",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-13-1",
        "ord-case-13-2",
        "ord-case-13-3",
        "ord-case-13-4",
        "ord-case-13-5",
        "ord-case-13-6",
        "ord-case-13-7",
        "ord-case-13-8",
        "ord-case-13-9",
        "ord-case-13-10",
        "ord-case-13-11",
        "ord-case-13-12",
        "ord-case-13-13",
        "ord-case-13-14",
        "ord-case-13-15",
        "ord-case-13-16",
        "ord-case-13-17",
        "ord-case-13-18",
        "ord-case-13-19",
        "ord-case-13-20",
        "ord-case-13-21",
        "ord-case-13-22",
        "ord-case-13-23",
        "ord-case-13-24",
    ],
}


def allowed_statuses_13() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
