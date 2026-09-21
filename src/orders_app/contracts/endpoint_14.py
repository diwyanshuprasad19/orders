"""OpenAPI contract fragment 14 for orders."""

CONTRACT_14 = {
    "id": "ord-14",
    "method": "PATCH",
    "path": "/v1/contract/14",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-14-1",
        "ord-case-14-2",
        "ord-case-14-3",
        "ord-case-14-4",
        "ord-case-14-5",
        "ord-case-14-6",
        "ord-case-14-7",
        "ord-case-14-8",
        "ord-case-14-9",
        "ord-case-14-10",
        "ord-case-14-11",
        "ord-case-14-12",
        "ord-case-14-13",
        "ord-case-14-14",
        "ord-case-14-15",
        "ord-case-14-16",
        "ord-case-14-17",
        "ord-case-14-18",
        "ord-case-14-19",
        "ord-case-14-20",
        "ord-case-14-21",
        "ord-case-14-22",
        "ord-case-14-23",
        "ord-case-14-24",
    ],
}


def allowed_statuses_14() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
