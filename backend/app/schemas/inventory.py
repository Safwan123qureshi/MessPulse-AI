from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class InventoryItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=100)
    quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="kg", max_length=50)
    purchase_price: Decimal = Field(default=0, ge=0)
    supplier: Optional[str] = Field(default=None, max_length=200)
    stock_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    minimum_stock: Decimal = Field(default=0, ge=0)
    is_active: bool = True


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=100)
    quantity: Optional[Decimal] = Field(default=None, ge=0)
    unit: Optional[str] = Field(default=None, max_length=50)
    purchase_price: Optional[Decimal] = Field(default=None, ge=0)
    supplier: Optional[str] = Field(default=None, max_length=200)
    stock_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    minimum_stock: Optional[Decimal] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    hostel_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True