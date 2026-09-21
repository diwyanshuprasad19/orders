"""initial orders schema

Revision ID: 0001
Revises:
Create Date: 2026-09-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(256), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("customer_id", sa.String(36), sa.ForeignKey("customers.id")),
        sa.Column("sku", sa.String(64), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("reservation_id", sa.String(36)),
        sa.Column("total_cents", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "order_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("order_id", sa.String(36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("payload", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "payments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("order_id", sa.String(36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), server_default="captured"),
        sa.Column("provider_ref", sa.String(128)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "shipments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("order_id", sa.String(36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("carrier", sa.String(64), server_default="UPS"),
        sa.Column("tracking", sa.String(128)),
        sa.Column("status", sa.String(32), server_default="label_created"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "refunds",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("order_id", sa.String(36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(256), server_default="customer_request"),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    for t in ("refunds", "shipments", "payments", "order_events", "orders", "customers"):
        op.drop_table(t)
