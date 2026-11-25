from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PurchaseItemBase(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200)
    quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="kg", max_length=50)
    unit_price: Decimal = Field(default=0, ge=0)
    total_price: Decimal = Field(default=0, ge=0)


class PurchaseItemCreate(PurchaseItemBase):
    pass


class PurchaseItemResponse(PurchaseItemBase):
    id: int
    purchase_id: int

    class Config:
        from_attributes = True


class PurchaseBase(BaseModel):
    supplier_id: Optional[int] = None
    purchase_date: datetime
    invoice_number: Optional[str] = Field(default=None, max_length=100)
    payment_status: str = Field(default="pending", max_length=20)
    subtotal: Decimal = Field(default=0, ge=0)
    tax: Decimal = Field(default=0, ge=0)
    discount: Decimal = Field(default=0, ge=0)
    total_amount: Decimal = Field(default=0, ge=0)
    notes: Optional[str] = None


class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate] = []


class PurchaseUpdate(BaseModel):
    payment_status: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = None


class PurchaseResponse(PurchaseBase):
    id: int
    hostel_id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[PurchaseItemResponse] = []

    class Config:
        from_attributes = True