import re
from datetime import datetime

from backend.app.services.ner import extract_entities


AMOUNT_PATTERN = re.compile(
    r"(?:₹|INR|Rs\.?)\s*([\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)

DATE_PATTERNS = [
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b"),
]


def extract_financial_fields(text: str) -> dict:
    """Extract financial fields from OCR/SMS text."""

    entities = extract_entities(text)

    amount = _extract_amount(text)
    transaction_date = _extract_date(text)

    merchant = None
    for entity in entities:
        if entity["entity"] == "ORG":
            merchant = entity["text"]
            break

    category = _categorize(merchant or text)

    return {
        "amount": amount,
        "merchant": merchant,
        "date": transaction_date,
        "category": category,
        "entities": entities,
    }


def _extract_amount(text: str) -> float | None:
    match = AMOUNT_PATTERN.search(text)

    if not match:
        return None

    return float(match.group(1).replace(",", ""))


def _extract_date(text: str) -> datetime | None:
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)

        if not match:
            continue

        value = match.group(1)

        for date_format in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue

    return None


def _categorize(text: str) -> str:
    normalized = text.lower()

    categories = {
        "Food": ("food", "restaurant", "cafe", "grocery", "mart"),
        "Transport": ("metro", "uber", "ola", "fuel", "taxi"),
        "Shopping": ("store", "shop", "market"),
        "Utilities": ("electric", "water", "internet"),
        "Salary": ("salary",),
    }

    for category, keywords in categories.items():
        if any(keyword in normalized for keyword in keywords):
            return category

    return "Other"