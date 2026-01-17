from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, String, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class RawTransaction(Base):
    __tablename__ = "raw_transactions"

    transaction_id = Column(String(64), primary_key=True)
    account_id = Column(String(64), nullable=False)
    transaction_timestamp = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    merchant = Column(String(256), nullable=False)
    merchant_category = Column(String(128), nullable=True)
    country = Column(String(2), nullable=False)
    payment_method = Column(String(64), nullable=True)
    channel = Column(String(64), nullable=True)
    status = Column(String(32), nullable=True)
    ingested_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CuratedTransaction(Base):
    __tablename__ = "curated_transactions"

    transaction_id = Column(String(64), primary_key=True)
    account_id = Column(String(64), nullable=False)
    transaction_timestamp = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    merchant = Column(String(256), nullable=False)
    country = Column(String(2), nullable=False)
    risk_flag = Column(Boolean, nullable=False, default=False)
    risk_reason = Column(Text, nullable=True)
    curated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
