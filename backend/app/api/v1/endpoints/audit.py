from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.common import AuditLogResponse
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_super_admin,
    get_hostel_or_404,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[AuditLogResponse])
def list_audit_logs(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    return db.query(AuditLog).filter(AuditLog.hostel_id == hostel_id).order_by(AuditLog.created_at.desc()).all()


@router.get("/platform", response_model=List[AuditLogResponse])
def list_platform_audit_logs(
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()