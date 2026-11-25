from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.hostel import Hostel
from app.models.attendance import Attendance
from app.models.meal import Meal
from app.models.booking import MealBooking
from app.models.food_waste import FoodWaste
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.user import User
from app.schemas.ai import PredictionResponse, RecommendationResponse, AIInsightsResponse, DemandPredictionRequest
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)
from decimal import Decimal
from datetime import datetime, timedelta

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/insights/{hostel_id}", response_model=AIInsightsResponse)
def get_ai_insights(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    predictions = (
        db.query(Prediction)
        .filter(Prediction.hostel_id == hostel_id)
        .order_by(Prediction.prediction_date.desc())
        .limit(20)
        .all()
    )
    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.hostel_id == hostel_id)
        .order_by(Recommendation.created_at.desc())
        .limit(20)
        .all()
    )
    return AIInsightsResponse(
        predictions=predictions,
        recommendations=recommendations,
        message="AI insights generated from hostel data",
    )


@router.post("/predict-demand/{hostel_id}", response_model=PredictionResponse)
def predict_demand(
    hostel_id: int,
    request: DemandPredictionRequest,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    from app.services.ai_service import predict_meal_demand, get_dashboard_stats
    prediction = predict_meal_demand(db, hostel_id, request.meal_type, request.prediction_date)
    if not prediction:
        raise HTTPException(status_code=400, detail="Insufficient historical data for prediction")
    return prediction


@router.get("/recommendations/{hostel_id}", response_model=List[RecommendationResponse])
def get_recommendations(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    return (
        db.query(Recommendation)
        .filter(Recommendation.hostel_id == hostel_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )


@router.post("/generate-recommendations/{hostel_id}", response_model=List[RecommendationResponse])
def generate_recommendations(
    hostel_id: int,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    from app.services.ai_service import generate_recommendations as gen_recs
    recs = gen_recs(db, hostel_id)
    return recs


@router.get("/dashboard-stats/{hostel_id}")
def dashboard_stats(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    stats = get_dashboard_stats(db, hostel_id)
    return stats