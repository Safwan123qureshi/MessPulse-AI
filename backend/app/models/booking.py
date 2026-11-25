from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class MealBooking(Base):
    __tablename__ = "meal_bookings"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    booking_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    status = Column(String(20), default="booked")  # booked, cancelled, served, no_show
    quantity = Column(Integer, default=1)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancellation_reason = Column(String(500), nullable=True)

    __table_args__ = (
        Index("ix_bookings_hostel_student_meal", "hostel_id", "student_id", "meal_id", unique=True),
        Index("ix_bookings_student_id", "student_id"),
        Index("ix_bookings_meal_id", "meal_id"),
        Index("ix_bookings_status", "status"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="meal_bookings")
    student = relationship("Student", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    meal = relationship("Meal", back_populates="bookings")