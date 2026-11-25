from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Numeric, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="SET NULL"), nullable=True, index=True)
    rating = Column(Numeric(3, 2), nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    feedback_type = Column(String(50), default="meal_rating")  # meal_rating, quality_concern, waste_report
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_feedback_hostel_student", "hostel_id", "student_id"),
        Index("ix_feedback_meal_id", "meal_id"),
        Index("ix_feedback_created_at", "created_at"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="feedback")
    student = relationship("Student", back_populates="feedback")
    meal = relationship("Meal")