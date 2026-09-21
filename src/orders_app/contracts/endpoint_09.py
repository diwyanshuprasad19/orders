"""OpenAPI contract fragment 09 for orders."""

CONTRACT_09 = {
    "id": "ord-09",
    "method": "GET",
    "path": "/v1/contract/09",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-9-1",
        "ord-case-9-2",
        "ord-case-9-3",
        "ord-case-9-4",
        "ord-case-9-5",
        "ord-case-9-6",
        "ord-case-9-7",
        "ord-case-9-8",
        "ord-case-9-9",
        "ord-case-9-10",
        "ord-case-9-11",
        "ord-case-9-12",
        "ord-case-9-13",
        "ord-case-9-14",
        "ord-case-9-15",
        "ord-case-9-16",
        "ord-case-9-17",
        "ord-case-9-18",
        "ord-case-9-19",
        "ord-case-9-20",
        "ord-case-9-21",
        "ord-case-9-22",
        "ord-case-9-23",
        "ord-case-9-24"
    ],
}


def allowed_statuses_09() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
