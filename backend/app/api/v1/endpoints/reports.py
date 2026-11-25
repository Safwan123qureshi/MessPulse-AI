from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.models.hostel import Hostel
from app.models.meal import Meal
from app.models.booking import MealBooking
from app.models.attendance import Attendance
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.food_waste import FoodWaste
from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)
import csv, io
from datetime import datetime, timedelta
from decimal import Decimal
from fastapi.responses import StreamingResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/daily-meal/{hostel_id}")
def daily_meal_report(
    hostel_id: int,
    date: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    report_date = datetime.strptime(date, "%Y-%m-%d")
    meals = db.query(Meal).filter(
        Meal.hostel_id == hostel_id,
        Meal.meal_date >= report_date,
        Meal.meal_date < report_date + timedelta(days=1),
    ).all()
    bookings = db.query(MealBooking).filter(
        MealBooking.hostel_id == hostel_id,
        MealBooking.booking_date >= report_date,
        MealBooking.booking_date < report_date + timedelta(days=1),
    ).all()
    attendance = db.query(Attendance).filter(
        Attendance.hostel_id == hostel_id,
        Attendance.attendance_date >= report_date,
        Attendance.attendance_date < report_date + timedelta(days=1),
    ).all()
    return {
        "date": date,
        "hostel_id": hostel_id,
        "meals": len(meals),
        "bookings": len(bookings),
        "attendance_records": len(attendance),
    }


@router.get("/weekly-consumption/{hostel_id}")
def weekly_consumption_report(
    hostel_id: int,
    start_date: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=7)
    meals = db.query(Meal).filter(
        Meal.hostel_id == hostel_id,
        Meal.meal_date >= start,
        Meal.meal_date < end,
    ).all()
    bookings = db.query(MealBooking).filter(
        MealBooking.hostel_id == hostel_id,
        MealBooking.booking_date >= start,
        MealBooking.booking_date < end,
    ).all()
    return {"period": f"{start_date} to {(end - timedelta(days=1)).strftime('%Y-%m-%d')}", "meals": len(meals), "bookings": len(bookings)}


@router.get("/monthly-expenses/{hostel_id}")
def monthly_expenses_report(
    hostel_id: int,
    month: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    start = datetime.strptime(month + "-01", "%Y-%m-%d")
    if month.endswith("-12"):
        end = datetime(int(month[:4]) + 1, 1, 1)
    else:
        end = datetime(int(month[:4]), int(month[5:]) + 1, 1)
    expenses = db.query(Expense).filter(
        Expense.hostel_id == hostel_id,
        Expense.expense_date >= start,
        Expense.expense_date < end,
    ).all()
    total = sum((e.amount or Decimal("0")) for e in expenses)
    return {"month": month, "total_expenses": total, "expense_count": len(expenses)}


@router.get("/budget/{hostel_id}")
def budget_report(
    hostel_id: int,
    month: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    budget = db.query(Budget).filter(Budget.hostel_id == hostel_id, Budget.month == month).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    utilization = Decimal("0")
    if budget.allocated_amount > 0:
        utilization = (budget.total_expenses / budget.allocated_amount * 100).quantize(Decimal("0.01"))
    return {
        "month": month,
        "allocated": budget.allocated_amount,
        "expenses": budget.total_expenses,
        "remaining": budget.remaining_amount,
        "utilization_percent": utilization,
    }


@router.get("/food-waste/{hostel_id}")
def food_waste_report(
    hostel_id: int,
    start_date: str,
    end_date: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    waste = db.query(FoodWaste).filter(
        FoodWaste.hostel_id == hostel_id,
        FoodWaste.waste_date >= start,
        FoodWaste.waste_date < end,
    ).all()
    total_prepared = sum((w.prepared_quantity or Decimal("0")) for w in waste)
    total_discarded = sum((w.discarded_quantity or Decimal("0")) for w in waste)
    return {
        "period": f"{start_date} to {end_date}",
        "records": len(waste),
        "total_prepared": total_prepared,
        "total_discarded": total_discarded,
    }


@router.get("/feedback/{hostel_id}")
def feedback_report(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    feedbacks = db.query(Feedback).filter(Feedback.hostel_id == hostel_id).all()
    avg_rating = Decimal("0")
    if feedbacks:
        avg_rating = sum((f.rating or Decimal("0")) for f in feedbacks) / len(feedbacks)
    return {"hostel_id": hostel_id, "feedback_count": len(feedbacks), "average_rating": avg_rating}


@router.get("/ai-forecast/{hostel_id}")
def ai_forecast_report(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    predictions = db.query(Prediction).filter(Prediction.hostel_id == hostel_id).all()
    return {"hostel_id": hostel_id, "predictions": len(predictions), "forecast_data": predictions}


@router.get("/export/csv/{hostel_id}/{report_type}")
def export_csv(
    hostel_id: int,
    report_type: str,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    output = io.StringIO()
    writer = csv.writer(output)
    if report_type == "expenses":
        writer.writerow(["ID", "Category", "Description", "Amount", "Date", "Status"])
        expenses = db.query(Expense).filter(Expense.hostel_id == hostel_id).all()
        for e in expenses:
            writer.writerow([e.id, e.category, e.description, e.amount, e.expense_date, e.payment_status])
    elif report_type == "bookings":
        writer.writerow(["ID", "Student ID", "Meal ID", "Status", "Quantity", "Date"])
        bookings = db.query(MealBooking).filter(MealBooking.hostel_id == hostel_id).all()
        for b in bookings:
            writer.writerow([b.id, b.student_id, b.meal_id, b.status, b.quantity, b.booking_date])
    elif report_type == "food-waste":
        writer.writerow(["ID", "Meal Type", "Date", "Prepared", "Discarded", "Waste %"])
        waste = db.query(FoodWaste).filter(FoodWaste.hostel_id == hostel_id).all()
        for w in waste:
            writer.writerow([w.id, w.meal_type, w.waste_date, w.prepared_quantity, w.discarded_quantity, w.waste_percentage])
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={report_type}_{hostel_id}.csv"},
    )