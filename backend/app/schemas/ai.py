from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PredictionResponse(BaseModel):
    id: int
    hostel_id: int
    meal_type: str
    prediction_date: datetime
    predicted_quantity: Decimal
    confidence: Optional[Decimal] = None
    method: Optional[str] = None
    data_points_used: int
    created_at: datetime

    class Config:
        from_attributes = True


class DemandPredictionRequest(BaseModel):
    meal_type: str
    prediction_date: datetime


class RecommendationResponse(BaseModel):
    id: int
    hostel_id: int
    title: str
    recommendation_text: str
    reason: Optional[str] = None
    supporting_data: Optional[str] = None
    confidence: Optional[str] = None
    suggested_action: Optional[str] = None
    category: Optional[str] = None
    is_implemented: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AIInsightsResponse(BaseModel):
    predictions: List[PredictionResponse]
    recommendations: List[RecommendationResponse]
    message: Optional[str] = None