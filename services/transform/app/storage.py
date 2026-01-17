from minio import Minio

from app.config import settings


def get_client() -> Minio:
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )


def fetch_object(object_key: str) -> bytes:
    client = get_client()
    response = client.get_object(settings.minio_bucket, object_key)
    data = response.read()
    response.close()
    response.release_conn()
    return data
