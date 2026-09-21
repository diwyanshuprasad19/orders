"""OpenAPI contract fragment 17 for orders."""

CONTRACT_17 = {
    "id": "ord-17",
    "method": "PATCH",
    "path": "/v1/contract/17",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-17-1",
        "ord-case-17-2",
        "ord-case-17-3",
        "ord-case-17-4",
        "ord-case-17-5",
        "ord-case-17-6",
        "ord-case-17-7",
        "ord-case-17-8",
        "ord-case-17-9",
        "ord-case-17-10",
        "ord-case-17-11",
        "ord-case-17-12",
        "ord-case-17-13",
        "ord-case-17-14",
        "ord-case-17-15",
        "ord-case-17-16",
        "ord-case-17-17",
        "ord-case-17-18",
        "ord-case-17-19",
        "ord-case-17-20",
        "ord-case-17-21",
        "ord-case-17-22",
        "ord-case-17-23",
        "ord-case-17-24",
    ],
}


def allowed_statuses_17() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
