from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type = Column(String(20), nullable=False, index=True)  # breakfast, lunch, dinner
    meal_date = Column(DateTime(timezone=True), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    estimated_cost = Column(Numeric(10, 2), default=0)
    available_quantity = Column(Integer, default=0)
    booking_deadline = Column(DateTime(timezone=True), nullable=True)
    is_published = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        Index("ix_meals_hostel_date_type", "hostel_id", "meal_date", "meal_type"),
        Index("ix_meals_hostel_published", "hostel_id", "is_published"),
    )

    # Relationships
    hostel = relationship("Hostel", back_populates="meals")
    creator = relationship("User")
    items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")
    bookings = relationship("MealBooking", back_populates="meal", cascade="all, delete-orphan")


class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Numeric(10, 2), default=0)
    unit = Column(String(50), default="portion")
    is_veg = Column(Boolean, default=True)

    # Relationships
    meal = relationship("Meal", back_populates="items")