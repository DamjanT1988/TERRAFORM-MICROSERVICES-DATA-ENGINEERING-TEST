import csv
import io
import logging
import uuid
from datetime import datetime, timezone
from typing import List

import orjson
from fastapi import FastAPI, File, HTTPException, UploadFile

from app.broker import publish_event
from app.config import settings
from app.logging import configure_logging
from app.schemas import IngestResponse, JsonIngestRequest, TransactionIn
from app.storage import upload_bytes, upload_stream


configure_logging(settings.log_level)
logger = logging.getLogger(settings.service_name)

app = FastAPI(title="Ingest Service", version="0.1.0")


def _object_key(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}/{ts}-{uuid.uuid4().hex}"


def _emit_event(object_key: str, count: int, source: str) -> None:
    payload = {
        "object_key": object_key,
        "bucket": settings.minio_bucket,
        "count": count,
        "source": source,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    publish_event(payload)


@app.post("/ingest/json", response_model=IngestResponse)
def ingest_json(request: JsonIngestRequest) -> IngestResponse:
    if not request.transactions:
        raise HTTPException(status_code=400, detail="No transactions provided")
    object_key = f"json/{_object_key('transactions')}.json"
    payload = orjson.dumps([item.model_dump(mode="json") for item in request.transactions])
    upload_bytes(object_key, payload, "application/json")
    _emit_event(object_key, len(request.transactions), "json")
    return IngestResponse(object_key=object_key, count=len(request.transactions))


@app.post("/ingest/csv", response_model=IngestResponse)
def ingest_csv(file: UploadFile = File(...)) -> IngestResponse:
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV file required")
    content = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty CSV file")
    try:
        decoded = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
        rows: List[TransactionIn] = [TransactionIn(**row) for row in reader]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {exc}") from exc

    object_key = f"csv/{_object_key('transactions')}.csv"
    upload_bytes(object_key, content, "text/csv")
    _emit_event(object_key, len(rows), "csv")
    return IngestResponse(object_key=object_key, count=len(rows))
