from fastapi import APIRouter
from app.api.v1.endpoints import auth, hostels, users, students, meals, bookings, attendance, inventory, purchases, expenses, budgets, food_waste, feedback, ai, bills, reports, audit

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(hostels.router, prefix="/hostels", tags=["hostels"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(food_waste.router, prefix="/food-waste", tags=["food-waste"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])