from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.attendance import Attendance
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[AttendanceResponse])
def list_attendance(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(Attendance).filter(Attendance.hostel_id == hostel_id).all()


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(
    hostel_id: int,
    attendance_in: AttendanceCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    existing = (
        db.query(Attendance)
        .filter(
            Attendance.hostel_id == hostel_id,
            Attendance.meal_type == attendance_in.meal_type,
            Attendance.attendance_date == attendance_in.attendance_date,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Attendance record already exists for this meal/date")
    att = Attendance(**attendance_in.model_dump(), hostel_id=hostel_id, recorded_by_id=current_user.id)
    db.add(att)
    db.commit()
    db.refresh(att)
    return att


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(
    hostel_id: int,
    attendance_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    att = (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id, Attendance.hostel_id == hostel_id)
        .first()
    )
    if not att:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return att


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    hostel_id: int,
    attendance_id: int,
    attendance_in: AttendanceUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    att = (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id, Attendance.hostel_id == hostel_id)
        .first()
    )
    if not att:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    update_data = attendance_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(att, field, value)
    db.commit()
    db.refresh(att)
    return att