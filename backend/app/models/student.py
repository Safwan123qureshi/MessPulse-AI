from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)  # hostel-specific student ID
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    room_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        Index("ix_students_hostel_id", "hostel_id"),
        Index("ix_students_student_id", "student_id"),
        Index("ix_students_user_id", "user_id"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="students")
    user = relationship("User", foreign_keys=[user_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id], back_populates="students_managed")
    bookings = relationship("MealBooking", back_populates="student", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="student", cascade="all, delete-orphan")