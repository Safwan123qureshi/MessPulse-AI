from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.inventory import InventoryItem
from app.models.user import User
from app.schemas.inventory import InventoryItemCreate, InventoryItemResponse, InventoryItemUpdate
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


@router.get("/", response_model=List[InventoryItemResponse])
def list_inventory(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(InventoryItem).filter(InventoryItem.hostel_id == hostel_id).all()


@router.post("/", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    hostel_id: int,
    item_in: InventoryItemCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    item = InventoryItem(**item_in.model_dump(), hostel_id=hostel_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=InventoryItemResponse)
def get_inventory_item(
    hostel_id: int,
    item_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    item = (
        db.query(InventoryItem)
        .filter(InventoryItem.id == item_id, InventoryItem.hostel_id == hostel_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.put("/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(
    hostel_id: int,
    item_id: int,
    item_in: InventoryItemUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    item = (
        db.query(InventoryItem)
        .filter(InventoryItem.id == item_id, InventoryItem.hostel_id == hostel_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item