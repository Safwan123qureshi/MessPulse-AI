"""Seed script for development - creates demo data."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.hostel import Hostel
from app.models.membership import Membership
from app.models.student import Student
from app.models.meal import Meal, MealItem
from app.models.booking import MealBooking
from app.models.attendance import Attendance
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.food_waste import FoodWaste
from app.models.feedback import Feedback
from datetime import datetime, timedelta
from decimal import Decimal


def seed():
    db = SessionLocal()
    try:
        # Create all tables (idempotent - ignore if already exist)
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Tables already exist (continuing): {e}")

        # Create super admin
        admin = User(
            email="admin@messpulse.ai",
            hashed_password=get_password_hash("Admin123!"),
            full_name="Platform Super Admin",
            role="super_admin",
            is_active=True,
            is_verified=True,
        )
        db.add(admin)
        db.flush()

        # Create demo hostels
        hostels_data = [
            {
                "name": "Hostel Alpha",
                "slug": "hostel-alpha",
                "address": "123 University Road, Campus Alpha",
                "contact_phone": "+92-300-1111111",
                "contact_email": "alpha@hostel.edu",
                "owner_name": "Ahmed Khan",
                "owner_email": "ahmed@hostel-alpha.edu",
                "owner_phone": "+92-300-1111112",
                "student_capacity": 200,
                "currency": "PKR",
            },
            {
                "name": "Hostel Beta",
                "slug": "hostel-beta",
                "address": "456 College Street, Campus Beta",
                "contact_phone": "+92-300-2222222",
                "contact_email": "beta@hostel.edu",
                "owner_name": "Fatima Ali",
                "owner_email": "fatima@hostel-beta.edu",
                "owner_phone": "+92-300-2222223",
                "student_capacity": 150,
                "currency": "PKR",
            },
            {
                "name": "Hostel Gamma",
                "slug": "hostel-gamma",
                "address": "789 Tech Park, Campus Gamma",
                "contact_phone": "+92-300-3333333",
                "contact_email": "gamma@hostel.edu",
                "owner_name": "Usman Tariq",
                "owner_email": "usman@hostel-gamma.edu",
                "owner_phone": "+92-300-3333334",
                "student_capacity": 180,
                "currency": "PKR",
            },
        ]

        created_hostels = []
        for hdata in hostels_data:
            hostel = Hostel(**hdata, is_active=True)
            db.add(hostel)
            db.flush()
            created_hostels.append(hostel)

        # Create owner users for each hostel
        owners = []
        for i, hostel in enumerate(created_hostels):
            owner = User(
                email=f"owner{i+1}@hostel.demo",
                hashed_password=get_password_hash("Owner123!"),
                full_name=hostel.owner_name,
                role="owner",
                is_active=True,
            )
            db.add(owner)
            db.flush()
            membership = Membership(
                user_id=owner.id,
                hostel_id=hostel.id,
                role="owner",
                is_active=True,
            )
            db.add(membership)
            owners.append(owner)

        # Create manager users
        managers = []
        for i, hostel in enumerate(created_hostels):
            manager = User(
                email=f"manager{i+1}@hostel.demo",
                hashed_password=get_password_hash("Manager123!"),
                full_name=f"Manager {hostel.name}",
                role="manager",
                is_active=True,
            )
            db.add(manager)
            db.flush()
            membership = Membership(
                user_id=manager.id,
                hostel_id=hostel.id,
                role="manager",
                is_active=True,
            )
            db.add(membership)
            managers.append(manager)

        # Create students for each hostel
        students = []
        for i, hostel in enumerate(created_hostels):
            for j in range(10):
                student = Student(
                    hostel_id=hostel.id,
                    student_id=f"H{i+1}S{j+1:03d}",
                    full_name=f"Student {j+1} {hostel.name}",
                    email=f"student{j+1}@hostel-{i+1}.demo",
                    phone=f"+92-300-{i+1}{j+1:03d}00",
                    room_number=f"{j+1:03d}",
                    is_active=True,
                )
                db.add(student)
                db.flush()
                students.append(student)

        db.commit()
        print("Seed data created successfully!")
        print(f"Super admin: admin@messpulse.ai / Admin123!")
        for i, owner in enumerate(owners):
            print(f"Hostel {i+1} owner: owner{i+1}@hostel.demo / Owner123!")
        for i, manager in enumerate(managers):
            print(f"Hostel {i+1} manager: manager{i+1}@hostel.demo / Manager123!")

    finally:
        db.close()


if __name__ == "__main__":
    seed()