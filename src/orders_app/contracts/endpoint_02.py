"""OpenAPI contract fragment 02 for orders."""

CONTRACT_02 = {
    "id": "ord-02",
    "method": "PATCH",
    "path": "/v1/contract/02",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-2-1",
        "ord-case-2-2",
        "ord-case-2-3",
        "ord-case-2-4",
        "ord-case-2-5",
        "ord-case-2-6",
        "ord-case-2-7",
        "ord-case-2-8",
        "ord-case-2-9",
        "ord-case-2-10",
        "ord-case-2-11",
        "ord-case-2-12",
        "ord-case-2-13",
        "ord-case-2-14",
        "ord-case-2-15",
        "ord-case-2-16",
        "ord-case-2-17",
        "ord-case-2-18",
        "ord-case-2-19",
        "ord-case-2-20",
        "ord-case-2-21",
        "ord-case-2-22",
        "ord-case-2-23",
        "ord-case-2-24"
    ],
}


def allowed_statuses_02() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
