from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "orders"
    database_url: str = "postgresql+psycopg://diwyanshuprasad@127.0.0.1:5432/orders_db"
    inventory_url: str = "http://127.0.0.1:8091"
    otel_service_name: str = "orders"
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    port: int = 8092
    cb_failure_threshold: int = 5
    cb_recovery_timeout: float = 15.0


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if url := os.getenv("DATABASE_URL"):
        object.__setattr__(s, "database_url", url)
    if inv := os.getenv("INVENTORY_URL"):
        object.__setattr__(s, "inventory_url", inv)
    return s
