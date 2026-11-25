# Models module - import all models to register them with SQLAlchemy
from app.models.hostel import Hostel  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.membership import Membership  # noqa: F401
from app.models.student import Student  # noqa: F401
from app.models.meal import Meal, MealItem  # noqa: F401
from app.models.booking import MealBooking  # noqa: F401
from app.models.attendance import Attendance  # noqa: F401
from app.models.inventory import InventoryItem  # noqa: F401
from app.models.supplier import Supplier  # noqa: F401
from app.models.purchase import Purchase, PurchaseItem  # noqa: F401
from app.models.expense import Expense  # noqa: F401
from app.models.budget import Budget  # noqa: F401
from app.models.food_waste import FoodWaste  # noqa: F401
from app.models.feedback import Feedback  # noqa: F401
from app.models.prediction import Prediction  # noqa: F401
from app.models.recommendation import Recommendation  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.bill import Bill, BillItem  # noqa: F401