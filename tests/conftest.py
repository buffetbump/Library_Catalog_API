"""
Конфигурационный файл pytest для настройки тестового окружения.
Определяет фикстуры для базы данных SQLite в памяти и тестового клиента API.
"""

import asyncio
import pytest
import pytest_asyncio

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from library_catalog.main import app
from library_catalog.core.database import get_db
from library_catalog.data.models.book import Base


# Используем быструю изолированную БД в оперативной памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    """ Создает единый цикл событий asyncio для всей сессии тестов """

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop

    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    """ Автоматически создает таблицы в тестовой базе перед стартом и удаляет после """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """ Фикстура для получения чистой сессии базы данных в каждом тесте """

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """ Тестовый клиент API, который подменяет реальный Postgres на SQLite в памяти """

    async def _get_test_db():
        yield db_session

    # Подменяем зависимость базы данных в FastAPI
    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Сбрасываем подмену после завершения теста
    app.dependency_overrides.clear()
