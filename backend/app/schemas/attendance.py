from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AttendanceBase(BaseModel):
    meal_type: str = Field(..., max_length=20)
    attendance_date: datetime
    expected_meals: int = Field(default=0, ge=0)
    actual_meals_served: int = Field(default=0, ge=0)
    prepared_quantity: Decimal = Field(default=0, ge=0)
    remaining_quantity: Decimal = Field(default=0, ge=0)
    discarded_quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="kg", max_length=50)


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    expected_meals: Optional[int] = Field(default=None, ge=0)
    actual_meals_served: Optional[int] = Field(default=None, ge=0)
    prepared_quantity: Optional[Decimal] = Field(default=None, ge=0)
    remaining_quantity: Optional[Decimal] = Field(default=None, ge=0)
    discarded_quantity: Optional[Decimal] = Field(default=None, ge=0)
    unit: Optional[str] = Field(default=None, max_length=50)


class AttendanceResponse(AttendanceBase):
    id: int
    hostel_id: int
    recorded_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True