from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.transaction import TransactionCreate, TransactionResponse
from backend.app.services.transaction import (
    create_transaction,
    delete_transaction,
    get_transaction,
    get_transactions,
    update_transaction,
)


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse)
def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    return create_transaction(db, transaction)


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return get_transaction(db, transaction_id)

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction_by_id(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    return update_transaction(db, transaction_id, transaction)

@router.delete("/{transaction_id}")
def delete_transaction_by_id(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return {"deleted": delete_transaction(db, transaction_id)}