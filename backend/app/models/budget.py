from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    month = Column(String(7), nullable=False, index=True)  # YYYY-MM
    allocated_amount = Column(Numeric(12, 2), nullable=False)
    total_expenses = Column(Numeric(12, 2), default=0)
    remaining_amount = Column(Numeric(12, 2), default=0)
    currency = Column(String(10), default="PKR")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_budgets_hostel_month", "hostel_id", "month", unique=True),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="budgets")