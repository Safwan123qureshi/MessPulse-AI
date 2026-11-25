from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MembershipBase(BaseModel):
    user_id: int
    hostel_id: int
    role: str = Field(..., max_length=50)


class MembershipCreate(MembershipBase):
    pass


class MembershipResponse(MembershipBase):
    id: int
    is_active: bool
    joined_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipUpdate(BaseModel):
    role: Optional[str] = Field(default=None, max_length=50)
    is_active: Optional[bool] = None


class UserMembershipResponse(BaseModel):
    id: int
    hostel_id: int
    hostel_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True