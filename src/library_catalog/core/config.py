"""
Модуль конфигурации приложения Library Catalog API.
Загружает, валидирует и кэширует переменные окружения из файла .env.
"""

from functools import lru_cache
from typing import Literal
from pydantic import PostgresDsn, computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings (BaseSettings):
    """ Класс настроек приложения с валидацией типов через Pydantic """

    # Обязательные поля конфигурации
    app_name: str = "Library Catalog API"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    database_url: PostgresDsn = Field(default=...)
    database_pool_size: int = 20
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    cors_origins: list[str] = ["*"]
    openlibrary_base_url: str = "https://openlibrary.org"
    openlibrary_timeout: float = 10.0

    # Настройки загрузки для pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    @property
    def is_production(self) -> bool:
        """ Проверяет, запущен ли проект в продакшене """

        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Возвращает кэшированный экземпляр настроек.
    Использует lru_cache, чтобы не перечитывать файл .env при каждом вызове.
    """

    return Settings()

settings = get_settings()