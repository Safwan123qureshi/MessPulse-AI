from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class FoodWasteBase(BaseModel):
    meal_type: str = Field(..., max_length=20)
    waste_date: datetime
    prepared_quantity: Decimal = Field(default=0, ge=0)
    consumed_quantity: Decimal = Field(default=0, ge=0)
    leftover_quantity: Decimal = Field(default=0, ge=0)
    discarded_quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="kg", max_length=50)
    reason: Optional[str] = None


class FoodWasteCreate(FoodWasteBase):
    pass


class FoodWasteUpdate(BaseModel):
    prepared_quantity: Optional[Decimal] = Field(default=None, ge=0)
    consumed_quantity: Optional[Decimal] = Field(default=None, ge=0)
    leftover_quantity: Optional[Decimal] = Field(default=None, ge=0)
    discarded_quantity: Optional[Decimal] = Field(default=None, ge=0)
    unit: Optional[str] = Field(default=None, max_length=50)
    reason: Optional[str] = None


class FoodWasteResponse(FoodWasteBase):
    id: int
    hostel_id: int
    waste_percentage: Decimal
    recorded_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True