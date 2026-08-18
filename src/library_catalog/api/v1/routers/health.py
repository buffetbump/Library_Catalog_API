"""
Роутер для проверки технического состояния приложения и базы данных.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from library_catalog.api.v1.schemas.common import HealthCheckResponse
from library_catalog.api.dependencies import DbSessionDep

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Проверить состояние сервиса и подключение к БД",
)
async def healt_check(db: DbSessionDep):
    """
    Проверить здоровье сервиса.
    
    Проверяет:
    - Сервис запущен
    - Подключение к БД работает
    """
    # Простой запрос к БД
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return HealthCheckResponse(
        status="healthy",
        database=db_status,
    )
