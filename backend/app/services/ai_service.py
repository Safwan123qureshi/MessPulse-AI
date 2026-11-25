"""AI Service - Meal demand prediction, recommendations, budget analysis."""
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.meal import Meal
from app.models.booking import MealBooking
from app.models.food_waste import FoodWaste
from app.models.budget import Budget
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.feedback import Feedback
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import statistics


def _round2(val):
    return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def predict_meal_demand(db: Session, hostel_id: int, meal_type: str, prediction_date: datetime):
    """Predict meal demand using historical attendance and booking data."""
    cutoff = prediction_date - timedelta(days=90)
    attendance_records = (
        db.query(Attendance)
        .filter(
            Attendance.hostel_id == hostel_id,
            Attendance.meal_type == meal_type,
            Attendance.attendance_date >= cutoff,
            Attendance.attendance_date < prediction_date,
        )
        .all()
    )
    booking_records = (
        db.query(MealBooking)
        .join(Meal, MealBooking.meal_id == Meal.id)
        .filter(
            Meal.hostel_id == hostel_id,
            Meal.meal_type == meal_type,
            MealBooking.booking_date >= cutoff,
            MealBooking.booking_date < prediction_date,
        )
        .all()
    )

    data_points = len(attendance_records) + len(booking_records)
    if data_points == 0:
        return None

    served_values = [float(a.actual_meals_served or 0) for a in attendance_records]
    booking_counts = len(booking_records)

    if served_values:
        avg_served = statistics.mean(served_values)
    else:
        avg_served = float(booking_counts) / max(len(set(b.booking_date.date() for b in booking_records)), 1) if booking_records else 0

    target_dow = prediction_date.weekday()
    dow_served = [
        float(a.actual_meals_served or 0)
        for a in attendance_records
        if a.attendance_date.weekday() == target_dow
    ]
    if dow_served:
        predicted = statistics.mean(dow_served)
        method = "day_of_week_average"
        confidence = Decimal("0.75")
    else:
        predicted = avg_served
        method = "moving_average"
        confidence = Decimal("0.50")

    predicted_qty = max(int(round(predicted)), 0)

    prediction = Prediction(
        hostel_id=hostel_id,
        meal_type=meal_type,
        prediction_date=prediction_date,
        predicted_quantity=predicted_qty,
        confidence=confidence,
        method=method,
        data_points_used=data_points,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def generate_recommendations(db: Session, hostel_id: int):
    """Generate AI recommendations for a hostel."""
    recommendations = []
    from app.models.student import Student

    waste_records = (
        db.query(FoodWaste)
        .filter(FoodWaste.hostel_id == hostel_id)
        .order_by(FoodWaste.waste_date.desc())
        .limit(30)
        .all()
    )
    if waste_records:
        high_waste = [w for w in waste_records if (w.waste_percentage or 0) > 30]
        if high_waste:
            meal_types = set(w.meal_type for w in high_waste)
            rec = Recommendation(
                hostel_id=hostel_id,
                title=f"High food waste detected in {', '.join(meal_types)}",
                recommendation_text="Review portion sizes and preparation quantities for meals with consistently high waste.",
                reason=f"{len(high_waste)} records show waste above 30%",
                supporting_data=f"Average waste: {_round2(sum((w.waste_percentage or 0) for w in high_waste) / len(high_waste))}%",
                confidence="medium",
                suggested_action="Reduce preparation quantity and monitor booking trends",
                category="waste",
            )
            db.add(rec)
            recommendations.append(rec)

    current_month = datetime.now().strftime("%Y-%m")
    budget = (
        db.query(Budget)
        .filter(Budget.hostel_id == hostel_id, Budget.month == current_month)
        .first()
    )
    if budget and budget.allocated_amount > 0:
        utilization = float(budget.total_expenses or 0) / float(budget.allocated_amount) * 100
        if utilization > 85:
            rec = Recommendation(
                hostel_id=hostel_id,
                title="Budget utilization above 85%",
                recommendation_text="Review expenses and consider cost-saving measures for the remainder of the month.",
                reason=f"Budget utilization at {utilization:.1f}%",
                supporting_data=f"Allocated: {budget.allocated_amount}, Spent: {budget.total_expenses}",
                confidence="high",
                suggested_action="Review top expense categories and reduce non-essential spending",
                category="budget",
            )
            db.add(rec)
            recommendations.append(rec)

    bookings = (
        db.query(MealBooking)
        .join(Meal, MealBooking.meal_id == Meal.id)
        .filter(Meal.hostel_id == hostel_id)
        .all()
    )
    if bookings:
        dow_bookings = {}
        for b in bookings:
            meal = db.query(Meal).filter(Meal.id == b.meal_id).first()
            if meal:
                dow = meal.meal_date.weekday()
                dow_bookings.setdefault(dow, 0)
                dow_bookings[dow] += 1
        if dow_bookings:
            min_dow = min(dow_bookings, key=dow_bookings.get)
            dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            rec = Recommendation(
                hostel_id=hostel_id,
                title=f"Lower demand on {dow_names[min_dow]}s",
                recommendation_text=f"Consider reducing preparation quantity for {dow_names[min_dow]}s based on historical booking patterns.",
                reason=f"Lowest booking count on {dow_names[min_dow]}s ({dow_bookings[min_dow]} bookings)",
                supporting_data=f"Day-of-week booking distribution: {dict(dow_bookings)}",
                confidence="medium",
                suggested_action="Adjust meal preparation quantities for low-demand days",
                category="demand",
            )
            db.add(rec)
            recommendations.append(rec)

    db.commit()
    for rec in recommendations:
        db.refresh(rec)
    return recommendations


def get_dashboard_stats(db: Session, hostel_id: int):
    """Get dashboard statistics for a hostel."""
    from app.models.student import Student
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    total_students = db.query(Student).filter(
        Student.hostel_id == hostel_id,
        Student.is_active == True,
    ).count()

    meals_booked_today = db.query(MealBooking).filter(
        MealBooking.hostel_id == hostel_id,
        MealBooking.booking_date >= now.replace(hour=0, minute=0, second=0),
    ).count()

    budget = db.query(Budget).filter(Budget.hostel_id == hostel_id, Budget.month == current_month).first()
    monthly_budget = budget.allocated_amount if budget else Decimal("0")
    monthly_expenses = budget.total_expenses if budget else Decimal("0")
    remaining_budget = budget.remaining_amount if budget else Decimal("0")

    today_waste = db.query(FoodWaste).filter(
        FoodWaste.hostel_id == hostel_id,
        FoodWaste.waste_date >= now.replace(hour=0, minute=0, second=0),
    ).all()
    total_waste_today = sum((w.discarded_quantity or Decimal("0")) for w in today_waste)

    feedbacks = db.query(Feedback).filter(Feedback.hostel_id == hostel_id).all()
    avg_rating = Decimal("0")
    if feedbacks:
        avg_rating = sum((f.rating or Decimal("0")) for f in feedbacks) / len(feedbacks)

    return {
        "total_students": total_students,
        "meals_booked_today": meals_booked_today,
        "monthly_budget": monthly_budget,
        "monthly_expenses": monthly_expenses,
        "remaining_budget": remaining_budget,
        "food_waste_today": total_waste_today,
        "average_rating": _round2(avg_rating),
    }