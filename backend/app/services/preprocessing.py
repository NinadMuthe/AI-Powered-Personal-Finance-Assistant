from sqlalchemy.orm import Session

from backend.app.models.transaction import Transaction

from collections import defaultdict
from datetime import date, timedelta


def load_transactions(db: Session) -> list[Transaction]:
    return db.query(Transaction).all()


def clean_transactions(
    transactions: list[Transaction],
) -> list[Transaction]:
    cleaned = []

    for transaction in transactions:
        if transaction.amount <= 0:
            continue

        if not transaction.transaction_type:
            continue

        if not transaction.transaction_date:
            continue

        transaction.category = normalize_category(transaction.category)

        cleaned.append(transaction)

    return cleaned



def aggregate_daily_expenses(
    transactions: list[Transaction],
) -> dict[date, float]:
    daily_expenses = defaultdict(float)

    for transaction in transactions:
        if transaction.transaction_type == "expense":
            transaction_day = transaction.transaction_date.date()
            daily_expenses[transaction_day] += transaction.amount

    return dict(sorted(daily_expenses.items()))

def fill_missing_dates(
    daily_expenses: dict[date, float],
) -> dict[date, float]:
    if not daily_expenses:
        return {}

    start_date = min(daily_expenses)
    end_date = max(daily_expenses)

    complete_daily_expenses = {}
    current_date = start_date

    while current_date <= end_date:
        complete_daily_expenses[current_date] = daily_expenses.get(
            current_date, 0.0
        )
        current_date += timedelta(days=1)

    return complete_daily_expenses

def normalize_category(category: str | None) -> str:
    if not category:
        return "Other"

    return category.strip().title()

def scale_daily_expenses(
    daily_expenses: dict[date, float],
) -> dict[date, float]:
    if not daily_expenses:
        return {}

    values = list(daily_expenses.values())

    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        return {day: 0.0 for day in daily_expenses}

    scaled_expenses = {}

    for day, amount in daily_expenses.items():
        scaled_value = (amount - min_value) / (max_value - min_value)
        scaled_expenses[day] = scaled_value

    return scaled_expenses