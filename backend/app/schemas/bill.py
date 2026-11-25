from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class BillItemBase(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200)
    quantity: Decimal = Field(default=0, ge=0)
    unit: str = Field(default="units", max_length=50)
    unit_price: Decimal = Field(default=0, ge=0)
    total_price: Decimal = Field(default=0, ge=0)


class BillItemCreate(BillItemBase):
    pass


class BillItemResponse(BillItemBase):
    id: int
    bill_id: int

    class Config:
        from_attributes = True


class BillBase(BaseModel):
    supplier_name: Optional[str] = Field(default=None, max_length=200)
    invoice_number: Optional[str] = Field(default=None, max_length=100)
    purchase_date: Optional[datetime] = None
    subtotal: Decimal = Field(default=0, ge=0)
    tax: Decimal = Field(default=0, ge=0)
    discount: Decimal = Field(default=0, ge=0)
    final_amount: Decimal = Field(default=0, ge=0)
    notes: Optional[str] = None


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    supplier_name: Optional[str] = Field(default=None, max_length=200)
    invoice_number: Optional[str] = Field(default=None, max_length=100)
    purchase_date: Optional[datetime] = None
    subtotal: Optional[Decimal] = Field(default=None, ge=0)
    tax: Optional[Decimal] = Field(default=None, ge=0)
    discount: Optional[Decimal] = Field(default=None, ge=0)
    final_amount: Optional[Decimal] = Field(default=None, ge=0)
    verification_status: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = None


class BillResponse(BillBase):
    id: int
    hostel_id: int
    uploaded_by_id: Optional[int] = None
    original_filename: str
    file_path: str
    file_type: str
    verification_status: str
    is_duplicate: bool
    duplicate_warning: Optional[str] = None
    ocr_raw_text: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[BillItemResponse] = []

    class Config:
        from_attributes = True


class BillUploadResponse(BaseModel):
    id: int
    hostel_id: int
    supplier_name: Optional[str]
    invoice_number: Optional[str]
    purchase_date: Optional[datetime]
    subtotal: Decimal
    tax: Decimal
    discount: Decimal
    final_amount: Decimal
    verification_status: str
    is_duplicate: bool
    duplicate_warning: Optional[str]
    items: List[BillItemResponse]
    message: str

    class Config:
        from_attributes = True