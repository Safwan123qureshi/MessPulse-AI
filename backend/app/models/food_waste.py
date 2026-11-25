from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class FoodWaste(Base):
    __tablename__ = "food_waste"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False, index=True)  # breakfast, lunch, dinner
    waste_date = Column(DateTime(timezone=True), nullable=False, index=True)
    prepared_quantity = Column(Numeric(10, 2), default=0)
    consumed_quantity = Column(Numeric(10, 2), default=0)
    leftover_quantity = Column(Numeric(10, 2), default=0)  # edible leftovers
    discarded_quantity = Column(Numeric(10, 2), default=0)  # thrown away
    unit = Column(String(50), default="kg")
    waste_percentage = Column(Numeric(5, 2), default=0)
    reason = Column(Text, nullable=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_food_waste_hostel_date_type", "hostel_id", "waste_date", "meal_type", unique=True),
        Index("ix_food_waste_date", "waste_date"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="food_waste")
    recorder = relationship("User")