from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.meal import Meal, MealItem
from app.models.user import User
from app.schemas.meal import MealCreate, MealResponse, MealUpdate, MealPublish
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


@router.get("/", response_model=List[MealResponse])
def list_meals(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    meals = db.query(Meal).filter(Meal.hostel_id == hostel_id).order_by(Meal.meal_date.desc()).all()
    return meals


@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
def create_meal(
    hostel_id: int,
    meal_in: MealCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    meal_data = meal_in.model_dump(exclude={"items"})
    meal = Meal(**meal_data, hostel_id=hostel_id, created_by_id=current_user.id)
    db.add(meal)
    db.flush()
    for item_in in meal_in.items:
        item = MealItem(**item_in.model_dump(), meal_id=meal.id)
        db.add(item)
    db.commit()
    db.refresh(meal)
    return meal


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(
    hostel_id: int,
    meal_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.hostel_id == hostel_id)
        .first()
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(
    hostel_id: int,
    meal_id: int,
    meal_in: MealUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.hostel_id == hostel_id)
        .first()
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    update_data = meal_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal, field, value)
    db.commit()
    db.refresh(meal)
    return meal


@router.patch("/{meal_id}/publish", response_model=MealResponse)
def publish_meal(
    hostel_id: int,
    meal_id: int,
    publish: MealPublish,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.hostel_id == hostel_id)
        .first()
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    meal.is_published = publish.is_published
    db.commit()
    db.refresh(meal)
    return meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    hostel_id: int,
    meal_id: int,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.hostel_id == hostel_id)
        .first()
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()