from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Numeric, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    original_filename = Column(String(300), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # jpg, jpeg, png, pdf
    supplier_name = Column(String(200), nullable=True)
    invoice_number = Column(String(100), nullable=True, index=True)
    purchase_date = Column(DateTime(timezone=True), nullable=True, index=True)
    subtotal = Column(Numeric(12, 2), default=0)
    tax = Column(Numeric(12, 2), default=0)
    discount = Column(Numeric(12, 2), default=0)
    final_amount = Column(Numeric(12, 2), default=0)
    verification_status = Column(String(20), default="pending")  # pending, verified, rejected
    is_duplicate = Column(Boolean, default=False)
    duplicate_warning = Column(Text, nullable=True)
    ocr_raw_text = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_bills_hostel_date", "hostel_id", "purchase_date"),
        Index("ix_bills_hostel_supplier", "hostel_id", "supplier_name"),
        Index("ix_bills_verification", "hostel_id", "verification_status"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="bills")
    uploaded_by_user = relationship("User", back_populates="bills")
    items = relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")
    expense = relationship("Expense", back_populates="bill", uselist=False)


class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id", ondelete="CASCADE"), nullable=False, index=True)
    item_name = Column(String(200), nullable=False)
    quantity = Column(Numeric(10, 2), default=0)
    unit = Column(String(50), default="units")
    unit_price = Column(Numeric(10, 2), default=0)
    total_price = Column(Numeric(12, 2), default=0)

    # Relationships
    bill = relationship("Bill", back_populates="items")