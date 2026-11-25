from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class MealItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="portion", max_length=50)
    is_veg: bool = True


class MealItemCreate(MealItemBase):
    pass


class MealItemResponse(MealItemBase):
    id: int
    meal_id: int

    class Config:
        from_attributes = True


class MealBase(BaseModel):
    meal_type: str = Field(..., max_length=20)
    meal_date: datetime
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    estimated_cost: Decimal = Field(default=0, ge=0)
    available_quantity: int = Field(default=0, ge=0)
    booking_deadline: Optional[datetime] = None
    is_published: bool = False


class MealCreate(MealBase):
    items: List[MealItemCreate] = []


class MealUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    estimated_cost: Optional[Decimal] = Field(default=None, ge=0)
    available_quantity: Optional[int] = Field(default=None, ge=0)
    booking_deadline: Optional[datetime] = None
    is_published: Optional[bool] = None
    is_active: Optional[bool] = None


class MealResponse(MealBase):
    id: int
    hostel_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[MealItemResponse] = []

    class Config:
        from_attributes = True


class MealPublish(BaseModel):
    is_published: bool