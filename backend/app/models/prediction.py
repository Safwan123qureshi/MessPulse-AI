from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False, index=True)
    prediction_date = Column(DateTime(timezone=True), nullable=False, index=True)
    predicted_quantity = Column(Numeric(10, 2), nullable=False)
    confidence = Column(Numeric(5, 2), nullable=True)
    method = Column(String(100), nullable=True)  # moving_average, day_of_week, sklearn_model
    data_points_used = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_predictions_hostel_date_type", "hostel_id", "prediction_date", "meal_type"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="predictions")