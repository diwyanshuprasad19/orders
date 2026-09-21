"""OpenAPI contract fragment 19 for orders."""

CONTRACT_19 = {
    "id": "ord-19",
    "method": "POST",
    "path": "/v1/contract/19",
    "circuit_breaker": True,
    "edge_cases": [
        "circuit open",
        "inventory 502",
        "ord-case-19-1",
        "ord-case-19-2",
        "ord-case-19-3",
        "ord-case-19-4",
        "ord-case-19-5",
        "ord-case-19-6",
        "ord-case-19-7",
        "ord-case-19-8",
        "ord-case-19-9",
        "ord-case-19-10",
        "ord-case-19-11",
        "ord-case-19-12",
        "ord-case-19-13",
        "ord-case-19-14",
        "ord-case-19-15",
        "ord-case-19-16",
        "ord-case-19-17",
        "ord-case-19-18",
        "ord-case-19-19",
        "ord-case-19-20",
        "ord-case-19-21",
        "ord-case-19-22",
        "ord-case-19-23",
        "ord-case-19-24",
    ],
}


def allowed_statuses_19() -> set[str]:
    return {"pending", "confirmed", "paid", "shipped", "delivered", "cancelled", "refunded"}
