from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(50), default="student")  # super_admin, owner, manager, student
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_role", "role"),
        Index("ix_users_is_active", "is_active"),
    )

    # Relationships
    memberships = relationship("Membership", back_populates="user", cascade="all, delete-orphan")
    students_managed = relationship("Student", back_populates="created_by_user", foreign_keys="Student.created_by_id")
    bookings = relationship("MealBooking", back_populates="user", cascade="all, delete-orphan")
    purchases = relationship("Purchase", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="uploaded_by_user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")