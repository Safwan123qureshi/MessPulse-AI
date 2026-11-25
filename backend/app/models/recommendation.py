from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Text, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    reason = Column(Text, nullable=True)
    supporting_data = Column(Text, nullable=True)  # JSON string
    confidence = Column(String(50), nullable=True)  # high, medium, low
    suggested_action = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # demand, waste, budget, menu
    is_implemented = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_recommendations_hostel", "hostel_id"),
        Index("ix_recommendations_category", "category"),
        Index("ix_recommendations_created_at", "created_at"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="recommendations")