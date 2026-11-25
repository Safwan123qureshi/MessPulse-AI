from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # food_purchase, gas, electricity, kitchen_supplies, other
    description = Column(String(500), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    expense_date = Column(DateTime(timezone=True), nullable=False, index=True)
    payment_status = Column(String(20), default="paid")
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="SET NULL"), nullable=True)
    bill_id = Column(Integer, ForeignKey("bills.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_expenses_hostel_date", "hostel_id", "expense_date"),
        Index("ix_expenses_hostel_category", "hostel_id", "category"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="expenses")
    purchase = relationship("Purchase")
    bill = relationship("Bill", back_populates="expense")
    user = relationship("User", back_populates="expenses")