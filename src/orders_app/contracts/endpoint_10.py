"""OpenAPI contract fragment 10 for orders."""

CONTRACT_10 = {
    "id": "ord-10",
    "method": "POST",
    "path": "/v1/contract/10",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-10-1",
        "ord-case-10-2",
        "ord-case-10-3",
        "ord-case-10-4",
        "ord-case-10-5",
        "ord-case-10-6",
        "ord-case-10-7",
        "ord-case-10-8",
        "ord-case-10-9",
        "ord-case-10-10",
        "ord-case-10-11",
        "ord-case-10-12",
        "ord-case-10-13",
        "ord-case-10-14",
        "ord-case-10-15",
        "ord-case-10-16",
        "ord-case-10-17",
        "ord-case-10-18",
        "ord-case-10-19",
        "ord-case-10-20",
        "ord-case-10-21",
        "ord-case-10-22",
        "ord-case-10-23",
        "ord-case-10-24",
    ],
}


def allowed_statuses_10() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
