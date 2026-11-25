from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ExpenseBase(BaseModel):
    category: str = Field(..., max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    amount: Decimal = Field(..., ge=0)
    expense_date: datetime
    payment_status: str = Field(default="paid", max_length=20)


class ExpenseCreate(ExpenseBase):
    purchase_id: Optional[int] = None
    bill_id: Optional[int] = None


class ExpenseUpdate(BaseModel):
    category: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    amount: Optional[Decimal] = Field(default=None, ge=0)
    expense_date: Optional[datetime] = None
    payment_status: Optional[str] = Field(default=None, max_length=20)


class ExpenseResponse(ExpenseBase):
    id: int
    hostel_id: int
    purchase_id: Optional[int] = None
    bill_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True