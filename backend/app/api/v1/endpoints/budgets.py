from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetUpdate
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


@router.get("/", response_model=List[BudgetResponse])
def list_budgets(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(Budget).filter(Budget.hostel_id == hostel_id).all()


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    hostel_id: int,
    budget_in: BudgetCreate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    existing = (
        db.query(Budget)
        .filter(Budget.hostel_id == hostel_id, Budget.month == budget_in.month)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this month")
    budget = Budget(**budget_in.model_dump(), hostel_id=hostel_id, remaining_amount=budget_in.allocated_amount)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/{month}", response_model=BudgetResponse)
def get_budget(
    hostel_id: int,
    month: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    budget = (
        db.query(Budget)
        .filter(Budget.hostel_id == hostel_id, Budget.month == month)
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/{month}", response_model=BudgetResponse)
def update_budget(
    hostel_id: int,
    month: str,
    budget_in: BudgetUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    budget = (
        db.query(Budget)
        .filter(Budget.hostel_id == hostel_id, Budget.month == month)
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    update_data = budget_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget