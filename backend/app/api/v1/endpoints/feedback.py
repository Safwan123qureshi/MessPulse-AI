from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.feedback import Feedback
from app.models.user import User
from app.models.student import Student
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackUpdate
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


@router.get("/", response_model=List[FeedbackResponse])
def list_feedback(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(Feedback).filter(Feedback.hostel_id == hostel_id).all()


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(
    hostel_id: int,
    feedback_in: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    student = (
        db.query(Student)
        .filter(Student.id == feedback_in.student_id, Student.hostel_id == hostel_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found in this hostel")
    feedback = Feedback(**feedback_in.model_dump(), hostel_id=hostel_id)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    hostel_id: int,
    feedback_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    feedback = (
        db.query(Feedback)
        .filter(Feedback.id == feedback_id, Feedback.hostel_id == hostel_id)
        .first()
    )
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    hostel_id: int,
    feedback_id: int,
    feedback_in: FeedbackUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    feedback = (
        db.query(Feedback)
        .filter(Feedback.id == feedback_id, Feedback.hostel_id == hostel_id)
        .first()
    )
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    update_data = feedback_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(feedback, field, value)
    db.commit()
    db.refresh(feedback)
    return feedback