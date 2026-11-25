from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Numeric, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(200), nullable=True)
    owner_name = Column(String(200), nullable=True)
    owner_email = Column(String(200), nullable=True)
    owner_phone = Column(String(50), nullable=True)
    student_capacity = Column(Integer, default=0)
    currency = Column(String(10), default="PKR")
    operating_days = Column(String(50), default="1,2,3,4,5,6")  # comma-separated weekdays (Mon=1)
    breakfast_time = Column(String(20), default="07:00")
    lunch_time = Column(String(20), default="12:00")
    dinner_time = Column(String(20), default="19:00")
    booking_cutoff_hours = Column(Integer, default=2)  # hours before meal
    is_active = Column(Boolean, default=True)
    is_suspended = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_hostels_slug", "slug"),
        Index("ix_hostels_is_active", "is_active"),
    )

    # Relationships
    memberships = relationship("Membership", back_populates="hostel", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="hostel", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="hostel", cascade="all, delete-orphan")
    meal_bookings = relationship("MealBooking", back_populates="hostel", cascade="all, delete-orphan")
    attendance = relationship("Attendance", back_populates="hostel", cascade="all, delete-orphan")
    inventory_items = relationship("InventoryItem", back_populates="hostel", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="hostel", cascade="all, delete-orphan")
    purchases = relationship("Purchase", back_populates="hostel", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="hostel", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="hostel", cascade="all, delete-orphan")
    food_waste = relationship("FoodWaste", back_populates="hostel", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="hostel", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="hostel", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="hostel", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="hostel", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="hostel", cascade="all, delete-orphan")