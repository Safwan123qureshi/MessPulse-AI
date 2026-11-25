from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    purchase_date = Column(DateTime(timezone=True), nullable=False, index=True)
    invoice_number = Column(String(100), nullable=True, index=True)
    payment_status = Column(String(20), default="pending")  # pending, paid, cancelled
    subtotal = Column(Numeric(12, 2), default=0)
    tax = Column(Numeric(12, 2), default=0)
    discount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_purchases_hostel_date", "hostel_id", "purchase_date"),
        Index("ix_purchases_invoice", "hostel_id", "invoice_number"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="purchases")
    supplier = relationship("Supplier", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False, index=True)
    item_name = Column(String(200), nullable=False)
    quantity = Column(Numeric(10, 2), default=0)
    unit = Column(String(50), default="kg")
    unit_price = Column(Numeric(10, 2), default=0)
    total_price = Column(Numeric(12, 2), default=0)

    # Relationships
    purchase = relationship("Purchase", back_populates="items")