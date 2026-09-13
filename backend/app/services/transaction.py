import csv
from io import StringIO

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.transaction import Transaction
from backend.app.schemas.transaction import TransactionCreate


class TransactionCSVImportError(ValueError):
    """Raised when a transaction CSV cannot be imported safely."""


REQUIRED_CSV_COLUMNS = {
    "amount",
    "transaction_type",
    "category",
    "description",
    "transaction_date",
    "source",
}


def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session) -> list[Transaction]:
    return list(db.scalars(select(Transaction)).all())


def import_transactions_from_csv(db: Session, csv_content: str) -> int:
    """Validate a CSV file completely, then save all of its transactions."""
    reader = csv.DictReader(StringIO(csv_content))

    if reader.fieldnames is None:
        raise TransactionCSVImportError("The CSV file must include a header row.")

    missing_columns = REQUIRED_CSV_COLUMNS - set(reader.fieldnames)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise TransactionCSVImportError(f"Missing required CSV columns: {missing}.")

    transactions: list[Transaction] = []
    for row_number, row in enumerate(reader, start=2):
        if not any(value and value.strip() for value in row.values()):
            continue

        try:
            transaction = TransactionCreate.model_validate(row)
        except ValidationError as error:
            raise TransactionCSVImportError(
                f"Invalid transaction on CSV row {row_number}: {error.errors()[0]['msg']}"
            ) from error

        transactions.append(Transaction(**transaction.model_dump()))

    if not transactions:
        raise TransactionCSVImportError("The CSV file contains no transaction rows.")

    try:
        db.add_all(transactions)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return len(transactions)

def get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    return db.get(Transaction, transaction_id)

def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: TransactionCreate,
) -> Transaction | None:
    db_transaction = db.get(Transaction, transaction_id)

    if db_transaction is None:
        return None

    for field, value in transaction.model_dump().items():
        setattr(db_transaction, field, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def delete_transaction(db: Session, transaction_id: int) -> bool:
    db_transaction = db.get(Transaction, transaction_id)

    if db_transaction is None:
        return False

    db.delete(db_transaction)
    db.commit()

    return True
