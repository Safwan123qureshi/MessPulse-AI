from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.booking import MealBooking
from app.models.meal import Meal
from app.models.student import Student
from app.models.user import User
from app.schemas.booking import MealBookingCreate, MealBookingResponse, MealBookingUpdate
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)
import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[MealBookingResponse])
def list_bookings(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    bookings = db.query(MealBooking).filter(MealBooking.hostel_id == hostel_id).all()
    return bookings


@router.post("/", response_model=MealBookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    hostel_id: int,
    booking_in: MealBookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)

    meal = db.query(Meal).filter(Meal.id == booking_in.meal_id, Meal.hostel_id == hostel_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found in this hostel")

    student = (
        db.query(Student)
        .filter(Student.id == booking_in.student_id if hasattr(booking_in, 'student_id') else True)
        .first()
    )
    # For students, they book for themselves; for managers, they can book for any student
    student_id = None
    if current_user.role == "student":
        student_rec = (
            db.query(Student)
            .filter(Student.user_id == current_user.id, Student.hostel_id == hostel_id)
            .first()
        )
        if not student_rec:
            raise HTTPException(status_code=404, detail="Student record not found")
        student_id = student_rec.id
    else:
        student_id = getattr(booking_in, 'student_id', None)
        if not student_id:
            raise HTTPException(status_code=400, detail="student_id required")

    # Check duplicate booking
    existing = (
        db.query(MealBooking)
        .filter(
            MealBooking.hostel_id == hostel_id,
            MealBooking.student_id == student_id,
            MealBooking.meal_id == booking_in.meal_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already booked for this meal")

    booking = MealBooking(
        hostel_id=hostel_id,
        student_id=student_id,
        user_id=current_user.id,
        meal_id=booking_in.meal_id,
        quantity=booking_in.quantity,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/{booking_id}", response_model=MealBookingResponse)
def get_booking(
    hostel_id: int,
    booking_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    booking = (
        db.query(MealBooking)
        .filter(MealBooking.id == booking_id, MealBooking.hostel_id == hostel_id)
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=MealBookingResponse)
def update_booking(
    hostel_id: int,
    booking_id: int,
    booking_in: MealBookingUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    booking = (
        db.query(MealBooking)
        .filter(MealBooking.id == booking_id, MealBooking.hostel_id == hostel_id)
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    update_data = booking_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)
    if update_data.get("status") == "cancelled":
        booking.cancelled_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    hostel_id: int,
    booking_id: int,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    booking = (
        db.query(MealBooking)
        .filter(MealBooking.id == booking_id, MealBooking.hostel_id == hostel_id)
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()