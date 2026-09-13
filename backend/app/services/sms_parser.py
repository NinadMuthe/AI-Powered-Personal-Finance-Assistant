import re

from backend.app.schemas.transaction import SMSMessage, TransactionCreate


class SMSParseError(ValueError):
    """Raised when a banking SMS does not contain a supported transaction."""


AMOUNT_PATTERN = re.compile(
    r"(?:₹|INR|Rs\.?)\s*([\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)
EXPENSE_PATTERN = re.compile(
    r"\b(debited|spent|paid|sent|purchase|withdrawn)\b", re.IGNORECASE
)
INCOME_PATTERN = re.compile(r"\b(credited|received)\b", re.IGNORECASE)
MERCHANT_PATTERNS = (
    re.compile(r"\b(?:to|at)\s+(.+?)(?:\s+on\s+|\.|$)", re.IGNORECASE),
    re.compile(r"\bfrom\s+(.+?)(?:\s+on\s+|\.|$)", re.IGNORECASE),
)


def parse_sms_message(message: SMSMessage) -> TransactionCreate:
    """Extract one transaction from a supported banking-style SMS message."""
    amount_match = AMOUNT_PATTERN.search(message.message)
    if amount_match is None:
        raise SMSParseError("could not find an INR amount")

    if EXPENSE_PATTERN.search(message.message):
        transaction_type = "expense"
    elif INCOME_PATTERN.search(message.message):
        transaction_type = "income"
    else:
        raise SMSParseError("could not determine whether the transaction is income or expense")

    description = _extract_description(message.message)
    return TransactionCreate(
        amount=float(amount_match.group(1).replace(",", "")),
        transaction_type=transaction_type,
        category=_categorize(description, transaction_type),
        description=description,
        transaction_date=message.received_at,
        source="sms",
    )


def _extract_description(message: str) -> str:
    for pattern in MERCHANT_PATTERNS:
        match = pattern.search(message)
        if match:
            return match.group(1).strip(" .")[:255]
    return "Synthetic SMS transaction"


def _categorize(description: str, transaction_type: str) -> str:
    normalized = description.lower()
    categories = {
        "Food": ("grocery", "mart", "restaurant", "cafe", "food"),
        "Transport": ("metro", "uber", "ola", "ride", "fuel"),
        "Utilities": ("electric", "water", "internet", "utility"),
        "Shopping": ("store", "shop", "market"),
        "Salary": ("salary",),
    }

    if transaction_type == "income" and "salary" in normalized:
        return "Salary"

    for category, keywords in categories.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Uncategorized"
