from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.purchase import Purchase, PurchaseItem
from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseResponse, PurchaseUpdate
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


@router.get("/", response_model=List[PurchaseResponse])
def list_purchases(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(Purchase).filter(Purchase.hostel_id == hostel_id).all()


@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    hostel_id: int,
    purchase_in: PurchaseCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    purchase_data = purchase_in.model_dump(exclude={"items"})
    purchase = Purchase(**purchase_data, hostel_id=hostel_id, user_id=current_user.id)
    db.add(purchase)
    db.flush()
    for item_in in purchase_in.items:
        item = PurchaseItem(**item_in.model_dump(), purchase_id=purchase.id)
        db.add(item)
    db.commit()
    db.refresh(purchase)
    return purchase


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    hostel_id: int,
    purchase_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    purchase = (
        db.query(Purchase)
        .filter(Purchase.id == purchase_id, Purchase.hostel_id == hostel_id)
        .first()
    )
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.put("/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(
    hostel_id: int,
    purchase_id: int,
    purchase_in: PurchaseUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    purchase = (
        db.query(Purchase)
        .filter(Purchase.id == purchase_id, Purchase.hostel_id == hostel_id)
        .first()
    )
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    update_data = purchase_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(purchase, field, value)
    db.commit()
    db.refresh(purchase)
    return purchase