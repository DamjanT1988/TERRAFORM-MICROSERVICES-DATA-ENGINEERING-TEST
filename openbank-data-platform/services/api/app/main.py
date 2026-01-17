import logging
from typing import List

from fastapi import Depends, FastAPI, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import require_api_key
from app.config import settings
from app.db import SessionLocal
from app.logging import configure_logging
from app.models import CuratedTransaction
from app.schemas import MerchantAggregate, TransactionOut


configure_logging(settings.log_level)
logger = logging.getLogger(settings.service_name)

app = FastAPI(title="API Service", version="0.1.0")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/transactions", response_model=List[TransactionOut], dependencies=[Depends(require_api_key)])
def list_transactions(
    db: Session = Depends(get_db),
    account_id: str | None = None,
    merchant: str | None = None,
    country: str | None = None,
    risk_flag: bool | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> List[TransactionOut]:
    query = select(CuratedTransaction)
    if account_id:
        query = query.where(CuratedTransaction.account_id == account_id)
    if merchant:
        query = query.where(CuratedTransaction.merchant.ilike(f"%{merchant}%"))
    if country:
        query = query.where(CuratedTransaction.country == country.upper())
    if risk_flag is not None:
        query = query.where(CuratedTransaction.risk_flag == risk_flag)
    query = query.limit(limit).offset(offset)
    rows = db.execute(query).scalars().all()
    return [TransactionOut.model_validate(row, from_attributes=True) for row in rows]


@app.get("/merchants/top", response_model=List[MerchantAggregate], dependencies=[Depends(require_api_key)])
def top_merchants(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
) -> List[MerchantAggregate]:
    query = (
        select(
            CuratedTransaction.merchant,
            func.sum(CuratedTransaction.amount).label("total_amount"),
            func.count(CuratedTransaction.transaction_id).label("count"),
        )
        .group_by(CuratedTransaction.merchant)
        .order_by(func.sum(CuratedTransaction.amount).desc())
        .limit(limit)
    )
    rows = db.execute(query).all()
    return [MerchantAggregate(merchant=row[0], total_amount=row[1], count=row[2]) for row in rows]


@app.get("/risk/flags", response_model=List[TransactionOut], dependencies=[Depends(require_api_key)])
def risk_flags(
    db: Session = Depends(get_db),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> List[TransactionOut]:
    query = (
        select(CuratedTransaction)
        .where(CuratedTransaction.risk_flag.is_(True))
        .limit(limit)
        .offset(offset)
    )
    rows = db.execute(query).scalars().all()
    return [TransactionOut.model_validate(row, from_attributes=True) for row in rows]
