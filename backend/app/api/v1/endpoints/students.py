from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.student import Student
from app.models.user import User
from app.models.membership import Membership
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
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


@router.get("/", response_model=List[StudentResponse])
def list_students(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    students = (
        db.query(Student)
        .filter(Student.hostel_id == hostel_id)
        .all()
    )
    return students


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    hostel_id: int,
    student_in: StudentCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    existing = (
        db.query(Student)
        .filter(Student.hostel_id == hostel_id, Student.student_id == student_in.student_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Student ID already exists in this hostel")
    student = Student(**student_in.model_dump(), hostel_id=hostel_id, created_by_id=current_user.id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    hostel_id: int,
    student_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.hostel_id == hostel_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    hostel_id: int,
    student_id: int,
    student_in: StudentUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.hostel_id == hostel_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    update_data = student_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    hostel_id: int,
    student_id: int,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.hostel_id == hostel_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()