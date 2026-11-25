from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class FeedbackBase(BaseModel):
    student_id: int
    meal_id: Optional[int] = None
    rating: Decimal = Field(..., ge=0, le=5)
    comment: Optional[str] = None
    feedback_type: str = Field(default="meal_rating", max_length=50)


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    rating: Optional[Decimal] = Field(default=None, ge=0, le=5)
    comment: Optional[str] = None
    feedback_type: Optional[str] = Field(default=None, max_length=50)
    is_resolved: Optional[bool] = None


class FeedbackResponse(FeedbackBase):
    id: int
    hostel_id: int
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True