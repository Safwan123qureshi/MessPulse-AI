from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MealBookingBase(BaseModel):
    meal_id: int
    quantity: int = Field(default=1, ge=1)


class MealBookingCreate(MealBookingBase):
    pass


class MealBookingUpdate(BaseModel):
    status: Optional[str] = Field(default=None, max_length=20)
    quantity: Optional[int] = Field(default=None, ge=1)


class MealBookingResponse(MealBookingBase):
    id: int
    hostel_id: int
    student_id: int
    booking_date: datetime
    status: str
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True