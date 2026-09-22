from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    email: str
    name: str


class CustomerOut(BaseModel):
    id: str
    email: str
    name: str
    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0)
    customer_id: str | None = None
    unit_price_cents: int = 0


class OrderStatusUpdate(BaseModel):
    status: str


class OrderOut(BaseModel):
    id: str
    sku: str
    qty: int
    status: str
    customer_id: str | None
    reservation_id: str | None
    total_cents: int
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class PayIn(BaseModel):
    amount_cents: int | None = None
    provider_ref: str | None = None


class ShipIn(BaseModel):
    carrier: str = "UPS"
    tracking: str | None = None


class RefundIn(BaseModel):
    order_id: str
    amount_cents: int = Field(gt=0)
    reason: str = "customer_request"


class EventOut(BaseModel):
    id: str
    event_type: str
    payload: str | None
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class PaymentOut(BaseModel):
    id: str
    order_id: str
    amount_cents: int
    status: str
    model_config = {"from_attributes": True}


class ShipmentOut(BaseModel):
    id: str
    order_id: str
    carrier: str
    tracking: str | None
    status: str
    model_config = {"from_attributes": True}
