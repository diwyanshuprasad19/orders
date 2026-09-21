"""OpenAPI contract fragment 16 for orders."""

CONTRACT_16 = {
    "id": "ord-16",
    "method": "POST",
    "path": "/v1/contract/16",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-16-1",
        "ord-case-16-2",
        "ord-case-16-3",
        "ord-case-16-4",
        "ord-case-16-5",
        "ord-case-16-6",
        "ord-case-16-7",
        "ord-case-16-8",
        "ord-case-16-9",
        "ord-case-16-10",
        "ord-case-16-11",
        "ord-case-16-12",
        "ord-case-16-13",
        "ord-case-16-14",
        "ord-case-16-15",
        "ord-case-16-16",
        "ord-case-16-17",
        "ord-case-16-18",
        "ord-case-16-19",
        "ord-case-16-20",
        "ord-case-16-21",
        "ord-case-16-22",
        "ord-case-16-23",
        "ord-case-16-24"
    ],
}


def allowed_statuses_16() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
