"""OCR Service - Local bill scanning using Tesseract OCR with fallback."""
import os
import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Dict, List, Optional

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def _parse_decimal(text: str) -> Decimal:
    """Parse a decimal value from text, handling currency symbols and commas."""
    if not text:
        return Decimal("0")
    cleaned = re.sub(r"[^\d.\-]", "", text)
    if not cleaned or cleaned == "-":
        return Decimal("0")
    try:
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _parse_date(text: str) -> Optional[datetime]:
    """Parse a date from text."""
    if not text:
        return None
    patterns = [
        r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})",
        r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            try:
                if len(groups[0]) == 4:
                    return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                else:
                    return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
            except ValueError:
                continue
    return None


def extract_bill_data(file_path: str, file_type: str) -> Dict:
    """Extract bill data from an uploaded file using OCR or manual fallback."""
    result = {
        "supplier_name": None,
        "invoice_number": None,
        "purchase_date": None,
        "subtotal": Decimal("0"),
        "tax": Decimal("0"),
        "discount": Decimal("0"),
        "final_amount": Decimal("0"),
        "items": [],
        "raw_text": "",
    }

    if not TESSERACT_AVAILABLE:
        result["raw_text"] = "OCR not available. Tesseract not installed. Please enter bill details manually."
        return result

    try:
        image = Image.open(file_path)
        raw_text = pytesseract.image_to_string(image)
        result["raw_text"] = raw_text

        # Extract supplier name (first non-empty line usually)
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        if lines:
            result["supplier_name"] = lines[0]

        # Extract invoice number
        inv_match = re.search(r"(?:invoice|bill|#|no)\s*[:.]?\s*([A-Za-z0-9\-]+)", raw_text, re.IGNORECASE)
        if inv_match:
            result["invoice_number"] = inv_match.group(1)

        # Extract date
        date_match = re.search(r"(?:date|dated)\s*[:.]?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{4})", raw_text, re.IGNORECASE)
        if date_match:
            result["purchase_date"] = _parse_date(date_match.group(1))

        # Extract amounts
        total_match = re.search(r"(?:total|grand total|amount)\s*[:.]?\s*([\d,.]+)", raw_text, re.IGNORECASE)
        if total_match:
            result["final_amount"] = _parse_decimal(total_match.group(1))

        subtotal_match = re.search(r"(?:subtotal)\s*[:.]?\s*([\d,.]+)", raw_text, re.IGNORECASE)
        if subtotal_match:
            result["subtotal"] = _parse_decimal(subtotal_match.group(1))

        tax_match = re.search(r"(?:tax|gst|vat)\s*[:.]?\s*([\d,.]+)", raw_text, re.IGNORECASE)
        if tax_match:
            result["tax"] = _parse_decimal(tax_match.group(1))

        discount_match = re.search(r"(?:discount)\s*[:.]?\s*([\d,.]+)", raw_text, re.IGNORECASE)
        if discount_match:
            result["discount"] = _parse_decimal(discount_match.group(1))

        # Extract line items (simple pattern: name qty price total)
        item_pattern = re.compile(r"(.+?)\s+(\d+(?:\.\d+)?)\s+([\d,.]+)\s+([\d,.]+)")
        for line in lines:
            match = item_pattern.search(line)
            if match:
                result["items"].append({
                    "name": match.group(1).strip(),
                    "quantity": _parse_decimal(match.group(2)),
                    "unit": "units",
                    "unit_price": _parse_decimal(match.group(3)),
                    "total_price": _parse_decimal(match.group(4)),
                })

    except Exception as e:
        result["raw_text"] = f"OCR error: {str(e)}. Please enter bill details manually."

    return result


def is_ocr_available() -> bool:
    return TESSERACT_AVAILABLE