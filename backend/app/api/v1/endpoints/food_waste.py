from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.food_waste import FoodWaste
from app.models.user import User
from app.schemas.food_waste import FoodWasteCreate, FoodWasteResponse, FoodWasteUpdate
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


@router.get("/", response_model=List[FoodWasteResponse])
def list_food_waste(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(FoodWaste).filter(FoodWaste.hostel_id == hostel_id).all()


@router.post("/", response_model=FoodWasteResponse, status_code=status.HTTP_201_CREATED)
def create_food_waste(
    hostel_id: int,
    waste_in: FoodWasteCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    total = waste_in.prepared_quantity
    consumed = waste_in.consumed_quantity
    leftover = waste_in.leftover_quantity
    discarded = waste_in.discarded_quantity
    waste_pct = Decimal("0")
    from decimal import Decimal
    if total > 0:
        waste_pct = ((leftover + discarded) / total * 100).quantize(Decimal("0.01"))
    waste = FoodWaste(
        **waste_in.model_dump(),
        hostel_id=hostel_id,
        waste_percentage=waste_pct,
        recorded_by_id=current_user.id,
    )
    db.add(waste)
    db.commit()
    db.refresh(waste)
    return waste


@router.get("/{waste_id}", response_model=FoodWasteResponse)
def get_food_waste(
    hostel_id: int,
    waste_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    waste = (
        db.query(FoodWaste)
        .filter(FoodWaste.id == waste_id, FoodWaste.hostel_id == hostel_id)
        .first()
    )
    if not waste:
        raise HTTPException(status_code=404, detail="Food waste record not found")
    return waste


@router.put("/{waste_id}", response_model=FoodWasteResponse)
def update_food_waste(
    hostel_id: int,
    waste_id: int,
    waste_in: FoodWasteUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    waste = (
        db.query(FoodWaste)
        .filter(FoodWaste.id == waste_id, FoodWaste.hostel_id == hostel_id)
        .first()
    )
    if not waste:
        raise HTTPException(status_code=404, detail="Food waste record not found")
    update_data = waste_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(waste, field, value)
    from decimal import Decimal
    total = waste.prepared_quantity
    if total > 0:
        waste.waste_percentage = ((waste.leftover_quantity + waste.discarded_quantity) / total * 100).quantize(Decimal("0.01"))
    db.commit()
    db.refresh(waste)
    return waste