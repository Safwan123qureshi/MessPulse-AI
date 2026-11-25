from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False, index=True)  # breakfast, lunch, dinner
    attendance_date = Column(DateTime(timezone=True), nullable=False, index=True)
    expected_meals = Column(Integer, default=0)
    actual_meals_served = Column(Integer, default=0)
    prepared_quantity = Column(Numeric(10, 2), default=0)
    remaining_quantity = Column(Numeric(10, 2), default=0)
    discarded_quantity = Column(Numeric(10, 2), default=0)
    unit = Column(String(50), default="kg")
    recorded_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_attendance_hostel_date_type", "hostel_id", "attendance_date", "meal_type", unique=True),
        Index("ix_attendance_date", "attendance_date"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="attendance")
    recorder = relationship("User")