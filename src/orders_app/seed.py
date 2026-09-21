from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from orders_app import models

DEMO_CUSTOMERS = [
    ("alice@example.com", "Alice Example"),
    ("bob@example.com", "Bob Example"),
    ("carol@example.com", "Carol Example"),
    ("dave@example.com", "Dave Example"),
    ("erin@example.com", "Erin Example"),
]


def seed_demo(db: Session) -> dict:
    created = 0
    for email, name in DEMO_CUSTOMERS:
        row = db.scalar(select(models.Customer).where(models.Customer.email == email))
        if not row:
            db.add(models.Customer(email=email, name=name))
            created += 1
    db.commit()
    return {"customers_created": created}
