from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class TransactionIn(BaseModel):
    transaction_id: str = Field(..., min_length=3)
    account_id: str
    transaction_timestamp: datetime
    amount: float
    currency: str = Field(..., min_length=3, max_length=3)
    merchant: str
    merchant_category: str | None = None
    country: str = Field(..., min_length=2, max_length=2)
    payment_method: str | None = None
    channel: str | None = None
    status: str | None = None


class IngestResponse(BaseModel):
    object_key: str
    count: int


class JsonIngestRequest(BaseModel):
    transactions: List[TransactionIn]
