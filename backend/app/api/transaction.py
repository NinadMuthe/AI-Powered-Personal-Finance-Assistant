from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.transaction import TransactionCreate, TransactionResponse
from backend.app.services.transaction import (
    create_transaction,
    delete_transaction,
    get_transaction,
    get_transactions,
    import_transactions_from_csv,
    TransactionCSVImportError,
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


@router.post("/import/csv", status_code=status.HTTP_201_CREATED)
async def import_transactions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Import a UTF-8 CSV of synthetic transactions into the database."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    try:
        csv_content = (await file.read()).decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise HTTPException(
            status_code=400,
            detail="The CSV file must be UTF-8 encoded.",
        ) from error

    try:
        imported_count = import_transactions_from_csv(db, csv_content)
    except TransactionCSVImportError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return {"imported_count": imported_count}

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
