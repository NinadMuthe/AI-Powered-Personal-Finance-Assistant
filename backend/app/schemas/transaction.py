from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    category: str | None = None
    description: str | None = None
    transaction_date: datetime
    source: str


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
