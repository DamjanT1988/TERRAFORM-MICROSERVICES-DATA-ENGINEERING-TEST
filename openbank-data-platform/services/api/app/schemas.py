from datetime import datetime

from pydantic import BaseModel


class TransactionOut(BaseModel):
    transaction_id: str
    account_id: str
    transaction_timestamp: datetime
    amount: float
    currency: str
    merchant: str
    country: str
    risk_flag: bool
    risk_reason: str | None


class MerchantAggregate(BaseModel):
    merchant: str
    total_amount: float
    count: int
