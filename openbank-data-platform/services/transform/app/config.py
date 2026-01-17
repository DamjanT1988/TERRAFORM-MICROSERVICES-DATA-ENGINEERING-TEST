from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRANSFORM_", env_file=".env")

    service_name: str = "transform-service"
    log_level: str = "INFO"

    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "raw-transactions"
    minio_secure: bool = False

    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    rabbitmq_exchange: str = "transactions"
    rabbitmq_queue: str = "transactions.transform"
    rabbitmq_routing_key: str = "ingest.created"

    database_url: str = "postgresql+psycopg2://postgres:postgres@postgres:5432/openbank"


settings = Settings()
