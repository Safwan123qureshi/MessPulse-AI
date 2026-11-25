from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class MessageResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list


class AuditLogResponse(BaseModel):
    id: int
    hostel_id: Optional[int]
    user_id: Optional[int]
    action: str
    entity_type: Optional[str]
    entity_id: Optional[int]
    details: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True