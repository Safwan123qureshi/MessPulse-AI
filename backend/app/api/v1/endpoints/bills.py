from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.bill import Bill, BillItem
from app.models.user import User
from app.schemas.bill import BillCreate, BillResponse, BillUpdate, BillUploadResponse, BillItemResponse
from app.models.budget import Budget
from app.api.deps import (
    get_db_session,
    get_current_user,
    require_hostel_member,
    require_hostel_role,
    get_hostel_or_404,
)
import os, uuid, shutil
from decimal import Decimal
from datetime import datetime

UPLOAD_DIR = "backend/uploads/bills"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload/{hostel_id}", response_model=BillUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_bill(
    hostel_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    get_hostel_or_404(hostel_id, db)
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG, PDF files allowed")
    file_id = str(uuid.uuid4())
    file_ext = file.filename.split(".")[-1].lower() if file.filename and "." in file.filename else "jpg"
    stored_name = f"{file_id}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    from app.services.ocr_service import extract_bill_data
    ocr_result = extract_bill_data(file_path, file_ext)
    duplicate_warning = None
    is_duplicate = False
    if ocr_result.get("invoice_number") or ocr_result.get("supplier_name"):
        existing = db.query(Bill).filter(Bill.hostel_id == hostel_id).all()
        for b in existing:
            if b.invoice_number == ocr_result.get("invoice_number") and b.supplier_name == ocr_result.get("supplier_name"):
                is_duplicate = True
                duplicate_warning = f"Possible duplicate: Bill #{b.id} from {b.supplier_name} on {b.purchase_date} for {b.final_amount}"
                break
    bill = Bill(
        hostel_id=hostel_id,
        uploaded_by_id=current_user.id,
        original_filename=file.filename or "unknown",
        file_path=file_path,
        file_type=file_ext,
        supplier_name=ocr_result.get("supplier_name"),
        invoice_number=ocr_result.get("invoice_number"),
        purchase_date=ocr_result.get("purchase_date"),
        subtotal=ocr_result.get("subtotal", Decimal("0")),
        tax=ocr_result.get("tax", Decimal("0")),
        discount=ocr_result.get("discount", Decimal("0")),
        final_amount=ocr_result.get("final_amount", Decimal("0")),
        verification_status="pending",
        is_duplicate=is_duplicate,
        duplicate_warning=duplicate_warning,
        ocr_raw_text=ocr_result.get("raw_text"),
    )
    db.add(bill)
    db.flush()
    for item in ocr_result.get("items", []):
        bill_item = BillItem(
            bill_id=bill.id,
            item_name=item.get("name", "Unknown"),
            quantity=item.get("quantity", Decimal("0")),
            unit=item.get("unit", "units"),
            unit_price=item.get("unit_price", Decimal("0")),
            total_price=item.get("total_price", Decimal("0")),
        )
        db.add(bill_item)
    db.commit()
    db.refresh(bill)
    return BillUploadResponse(
        id=bill.id, hostel_id=bill.hostel_id, supplier_name=bill.supplier_name,
        invoice_number=bill.invoice_number, purchase_date=bill.purchase_date,
        subtotal=bill.subtotal, tax=bill.tax, discount=bill.discount,
        final_amount=bill.final_amount, verification_status=bill.verification_status,
        is_duplicate=bill.is_duplicate, duplicate_warning=bill.duplicate_warning,
        items=bill.items,
        message="Bill uploaded successfully. Please review and verify before finalizing.",
    )


@router.get("/", response_model=List[BillResponse])
def list_bills(
    hostel_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    return db.query(Bill).filter(Bill.hostel_id == hostel_id).order_by(Bill.created_at.desc()).all()


@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(
    hostel_id: int,
    bill_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.hostel_id == hostel_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.put("/{bill_id}/verify", response_model=BillResponse)
def verify_bill(
    hostel_id: int,
    bill_id: int,
    bill_in: BillUpdate,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.hostel_id == hostel_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    update_data = bill_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bill, field, value)
    items = db.query(BillItem).filter(BillItem.bill_id == bill.id).all()
    calculated_subtotal = sum((i.total_price or Decimal("0")) for i in items)
    bill.subtotal = calculated_subtotal
    bill.verification_status = "verified"
    db.commit()
    db.refresh(bill)
    from app.models.expense import Expense
    expense = Expense(
        hostel_id=hostel_id,
        category="food_purchase",
        description=f"Bill #{bill.id} - {bill.supplier_name or 'Supplier'}",
        amount=bill.final_amount,
        expense_date=bill.purchase_date or datetime.now(),
        payment_status="paid",
        bill_id=bill.id,
        user_id=current_user.id,
    )
    db.add(expense)
    if bill.purchase_date:
        month_str = bill.purchase_date.strftime("%Y-%m")
        budget = db.query(Budget).filter(Budget.hostel_id == hostel_id, Budget.month == month_str).first()
        if budget:
            budget.total_expenses = (budget.total_expenses or Decimal("0")) + bill.final_amount
            budget.remaining_amount = (budget.allocated_amount or Decimal("0")) - budget.total_expenses
    db.commit()
    return bill


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(
    hostel_id: int,
    bill_id: int,
    current_user: User = Depends(require_hostel_role),
    db: Session = Depends(get_db_session),
):
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.hostel_id == hostel_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    if os.path.exists(bill.file_path):
        os.remove(bill.file_path)
    db.delete(bill)
    db.commit()


@router.get("/{bill_id}/file")
def get_bill_file(
    hostel_id: int,
    bill_id: int,
    current_user: User = Depends(require_hostel_member),
    db: Session = Depends(get_db_session),
):
    from fastapi.responses import FileResponse
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.hostel_id == hostel_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    if not os.path.exists(bill.file_path):
        raise HTTPException(status_code=404, detail="Bill file not found")
    return FileResponse(bill.file_path, filename=bill.original_filename)