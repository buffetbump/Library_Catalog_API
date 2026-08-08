"""
Модуль настройки асинхронного подключения к базе данных PostgreSQL.
Использует асинхронный движок SQLAlchemy 2.0 и драйвер asyncpg.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from library_catalog.core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для всех декларативных ORM-моделей приложения.
    От него мы будем наследовать все будущие таблицы (например, модель Book).
    """

    pass

# Инициализирует асинхронный движок базы данных
engine = create_async_engine(
    str(settings.database_url),
    pool_size=settings.database_pool_size,
    echo=settings.debug,
)

# Фабрика для конвеерной сборки асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """ 
    Генератор асинхронных сессий базы данных для Dependency Injection.
    Гарантирует автоматический откат транзакции при возникновении ошибок
    и безопасное закрытие соединения после выполнения любого запроса.
    """

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def dispose_engine() -> None:
    """
    Корректно закрывает все удерживаемые соединения в пуле базы данных.
    Вызывается при очистке системных ресурсов во время остановки приложения.
    """

    await engine.dispose()

