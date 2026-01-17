from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env")

    service_name: str = "api-service"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg2://postgres:postgres@postgres:5432/openbank"
    api_key: str = "local-dev-key"


settings = Settings()
