from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=True)
    quantity = Column(Numeric(10, 2), default=0)
    unit = Column(String(50), default="kg")
    purchase_price = Column(Numeric(10, 2), default=0)
    supplier = Column(String(200), nullable=True)
    stock_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    minimum_stock = Column(Numeric(10, 2), default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_inventory_hostel_name", "hostel_id", "name"),
        Index("ix_inventory_hostel_category", "hostel_id", "category"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="inventory_items")