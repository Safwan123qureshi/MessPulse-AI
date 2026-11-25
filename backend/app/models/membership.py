from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # owner, manager, student
    is_active = Column(Boolean, default=True)
    invited_at = Column(DateTime(timezone=True), server_default=func.now())
    joined_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_memberships_user_hostel", "user_id", "hostel_id", unique=True),
        Index("ix_memberships_hostel_id", "hostel_id"),
        Index("ix_memberships_user_id", "user_id"),
    )

    # Relationships
    user = relationship("User", back_populates="memberships")
    hostel = relationship("Hostel", back_populates="memberships")