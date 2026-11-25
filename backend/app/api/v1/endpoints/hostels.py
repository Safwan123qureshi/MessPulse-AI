from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.hostel import Hostel
from app.models.membership import Membership
from app.models.user import User
from app.schemas.hostel import HostelCreate, HostelResponse, HostelUpdate, HostelListResponse
from app.schemas.user import UserResponse
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_super_admin,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)
from app.core.security import get_password_hash

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=HostelResponse, status_code=status.HTTP_201_CREATED)
def create_hostel(
    hostel_in: HostelCreate,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    existing = db.query(Hostel).filter(Hostel.slug == hostel_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Hostel slug already exists")
    hostel = Hostel(**hostel_in.model_dump())
    db.add(hostel)
    db.commit()
    db.refresh(hostel)
    from app.models.audit_log import AuditLog
    audit = AuditLog(
        hostel_id=hostel.id,
        user_id=current_user.id,
        action="hostel_created",
        entity_type="hostel",
        entity_id=hostel.id,
        details=f"Hostel '{hostel.name}' created",
    )
    db.add(audit)
    db.commit()
    return hostel


@router.get("/", response_model=List[HostelListResponse])
def list_hostels(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    if current_user.role == "super_admin":
        hostels = db.query(Hostel).all()
    else:
        memberships = (
            db.query(Membership)
            .filter(Membership.user_id == current_user.id, Membership.is_active == True)
            .all()
        )
        hostel_ids = [m.hostel_id for m in memberships]
        hostels = db.query(Hostel).filter(Hostel.id.in_(hostel_ids)).all() if hostel_ids else []
    return [
        HostelListResponse(
            id=h.id, name=h.name, slug=h.slug, is_active=h.is_active,
            is_suspended=h.is_suspended, student_capacity=h.student_capacity,
            created_at=h.created_at,
        )
        for h in hostels
    ]


@router.get("/{hostel_id}", response_model=HostelResponse)
def get_hostel(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    return hostel


@router.put("/{hostel_id}", response_model=HostelResponse)
def update_hostel(
    hostel_id: int,
    hostel_in: HostelUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    update_data = hostel_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hostel, field, value)
    db.commit()
    db.refresh(hostel)
    return hostel


@router.delete("/{hostel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hostel(
    hostel_id: int,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    db.delete(hostel)
    db.commit()


@router.post("/{hostel_id}/suspend", response_model=HostelResponse)
def suspend_hostel(
    hostel_id: int,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    hostel.is_suspended = True
    db.commit()
    db.refresh(hostel)
    return hostel


@router.post("/{hostel_id}/activate", response_model=HostelResponse)
def activate_hostel(
    hostel_id: int,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    hostel.is_suspended = False
    db.commit()
    db.refresh(hostel)
    return hostel


@router.get("/{hostel_id}/members", response_model=List[UserResponse])
def get_hostel_members(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    memberships = (
        db.query(Membership)
        .filter(Membership.hostel_id == hostel_id, Membership.is_active == True)
        .all()
    )
    user_ids = [m.user_id for m in memberships]
    if not user_ids:
        return []
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    return users


@router.post("/{hostel_id}/members", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_hostel_member(
    hostel_id: int,
    user_id: int,
    role: str = "member",
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    hostel = get_hostel_or_404(hostel_id, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = (
        db.query(Membership)
        .filter(Membership.user_id == user_id, Membership.hostel_id == hostel_id)
        .first()
    )
    if existing:
        existing.is_active = True
        existing.role = role
        db.commit()
        db.refresh(existing)
        return user
    membership = Membership(user_id=user_id, hostel_id=hostel_id, role=role)
    db.add(membership)
    db.commit()
    return user