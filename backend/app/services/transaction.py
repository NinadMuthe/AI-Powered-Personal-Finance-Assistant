from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.transaction import Transaction
from backend.app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session) -> list[Transaction]:
    return list(db.scalars(select(Transaction)).all())

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