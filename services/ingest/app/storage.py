from io import BytesIO
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from app.config import settings


def get_client() -> Minio:
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )


def ensure_bucket(client: Minio) -> None:
    if not client.bucket_exists(settings.minio_bucket):
        client.make_bucket(settings.minio_bucket)


def upload_bytes(object_key: str, data: bytes, content_type: str) -> None:
    client = get_client()
    ensure_bucket(client)
    client.put_object(
        settings.minio_bucket,
        object_key,
        data=BytesIO(data),
        length=len(data),
        content_type=content_type,
    )


def upload_stream(object_key: str, fileobj: BinaryIO, size: int, content_type: str) -> None:
    client = get_client()
    ensure_bucket(client)
    client.put_object(
        settings.minio_bucket,
        object_key,
        data=fileobj,
        length=size,
        content_type=content_type,
    )
