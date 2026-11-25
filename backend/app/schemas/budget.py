from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class BudgetBase(BaseModel):
    month: str = Field(..., max_length=7, pattern=r"^\d{4}-\d{2}$")
    allocated_amount: Decimal = Field(..., ge=0)
    currency: str = Field(default="PKR", max_length=10)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    allocated_amount: Optional[Decimal] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, max_length=10)
    is_active: Optional[bool] = None


class BudgetResponse(BudgetBase):
    id: int
    hostel_id: int
    total_expenses: Decimal
    remaining_amount: Decimal
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True