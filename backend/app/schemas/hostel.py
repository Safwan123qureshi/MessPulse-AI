from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class HostelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    owner_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    owner_phone: Optional[str] = None
    student_capacity: int = Field(default=0, ge=0)
    currency: str = Field(default="PKR", max_length=10)
    operating_days: str = Field(default="1,2,3,4,5,6")
    breakfast_time: str = Field(default="07:00")
    lunch_time: str = Field(default="12:00")
    dinner_time: str = Field(default="19:00")
    booking_cutoff_hours: int = Field(default=2, ge=0)


class HostelCreate(HostelBase):
    pass


class HostelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    owner_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    owner_phone: Optional[str] = None
    student_capacity: Optional[int] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, max_length=10)
    operating_days: Optional[str] = None
    breakfast_time: Optional[str] = None
    lunch_time: Optional[str] = None
    dinner_time: Optional[str] = None
    booking_cutoff_hours: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None
    is_suspended: Optional[bool] = None


class HostelResponse(HostelBase):
    id: int
    is_active: bool
    is_suspended: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HostelListResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    is_suspended: bool
    student_capacity: int
    created_at: datetime

    class Config:
        from_attributes = True