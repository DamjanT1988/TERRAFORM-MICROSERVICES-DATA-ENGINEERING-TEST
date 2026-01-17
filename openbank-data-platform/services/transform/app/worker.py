import io
import logging
from datetime import datetime

import orjson
import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from app.broker import start_consumer
from app.config import settings
from app.db import SessionLocal
from app.logging import configure_logging
from app.models import CuratedTransaction, RawTransaction
from app.risk import assess_risk
from app.storage import fetch_object
from app.validation import transaction_schema


configure_logging(settings.log_level)
logger = logging.getLogger(settings.service_name)


def _load_dataframe(object_key: str) -> pd.DataFrame:
    payload = fetch_object(object_key)
    if object_key.endswith(".json"):
        data = orjson.loads(payload)
        return pd.DataFrame(data)
    if object_key.endswith(".csv"):
        return pd.read_csv(io.BytesIO(payload))
    raise ValueError(f"Unsupported object format: {object_key}")


def _persist_records(records: list[dict]) -> None:
    session = SessionLocal()
    try:
        if not records:
            return
        raw_insert = insert(RawTransaction).values(records)
        raw_insert = raw_insert.on_conflict_do_nothing(index_elements=["transaction_id"])
        session.execute(raw_insert)

        curated_rows = []
        for row in records:
            risk_flag, risk_reason = assess_risk(row["amount"], row["country"], row["merchant"])
            curated_rows.append(
                {
                    "transaction_id": row["transaction_id"],
                    "account_id": row["account_id"],
                    "transaction_timestamp": row["transaction_timestamp"],
                    "amount": row["amount"],
                    "currency": row["currency"],
                    "merchant": row["merchant"],
                    "country": row["country"],
                    "risk_flag": risk_flag,
                    "risk_reason": risk_reason,
                    "curated_at": datetime.utcnow(),
                }
            )

        curated_insert = insert(CuratedTransaction).values(curated_rows)
        curated_insert = curated_insert.on_conflict_do_nothing(index_elements=["transaction_id"])
        session.execute(curated_insert)
        session.commit()
    except Exception:  # noqa: BLE001
        session.rollback()
        raise
    finally:
        session.close()


def _process_message(payload: dict) -> None:
    object_key = payload.get("object_key")
    if not object_key:
        logger.warning("Missing object_key in payload: %s", payload)
        return

    df = _load_dataframe(object_key)
    df = transaction_schema.validate(df, lazy=True)
    df = df.drop_duplicates(subset=["transaction_id"])
    df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"], utc=False)

    records = df.to_dict(orient="records")
    _persist_records(records)
    logger.info("Processed %s records from %s", len(records), object_key)


def main() -> None:
    logger.info("Starting transform worker")
    start_consumer(_process_message)


if __name__ == "__main__":
    main()
