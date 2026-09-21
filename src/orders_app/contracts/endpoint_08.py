"""OpenAPI contract fragment 08 for orders."""

CONTRACT_08 = {
    "id": "ord-08",
    "method": "PATCH",
    "path": "/v1/contract/08",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-8-1",
        "ord-case-8-2",
        "ord-case-8-3",
        "ord-case-8-4",
        "ord-case-8-5",
        "ord-case-8-6",
        "ord-case-8-7",
        "ord-case-8-8",
        "ord-case-8-9",
        "ord-case-8-10",
        "ord-case-8-11",
        "ord-case-8-12",
        "ord-case-8-13",
        "ord-case-8-14",
        "ord-case-8-15",
        "ord-case-8-16",
        "ord-case-8-17",
        "ord-case-8-18",
        "ord-case-8-19",
        "ord-case-8-20",
        "ord-case-8-21",
        "ord-case-8-22",
        "ord-case-8-23",
        "ord-case-8-24"
    ],
}


def allowed_statuses_08() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
