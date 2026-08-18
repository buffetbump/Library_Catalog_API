"""
Модуль контейнера зависимостей для сборки и связывания слоев приложения.
Обеспечивает автоматическое внедрение зависимостей через механизм FastAPI Depends.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from library_catalog.core.database import get_db
from library_catalog.data.repositories.book_repository import BookRepository
from library_catalog.domain.services.book_service import BookService
from library_catalog.external.openlibrary.client import OpenLibraryClient
from library_catalog.core.config import settings


# ========== EXTERNAL CLIENTS (Singletons) ==========

@lru_cache
def get_openlibrary_client() -> OpenLibraryClient:
    """
    Получить singleton OpenLibraryClient.
    lru_cache создает клиент один раз и переиспользует.
    """

    return OpenLibraryClient(
        base_url=settings.openlibrary_base_url,
        timeout=settings.openlibrary_timeout,
    )


# ========== REPOSITORIES ==========

async def get_book_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> BookRepository:
    """
    Создает экземпляр репозитория книг для текущей сессии базы данных
    """

    return BookRepository(db)


# ========== SERVICES ==========

async def get_book_service(
    book_repo: Annotated[BookRepository, Depends(get_book_repository)],
    ol_client: Annotated[OpenLibraryClient, Depends(get_openlibrary_client)],
) -> BookService:
    """
    Создать BookService с внедренными зависимостями.
    
    FastAPI автоматически разрешит все зависимости:
    1. get_db() создаст AsyncSession
    2. get_book_repository() создаст BookRepository с session
    3. get_openlibrary_client() вернет singleton клиент
    4. Все внедрится в BookService
    """

    return BookService(
        book_repository=book_repo,
        openlibrary_client=ol_client,
    )


# Псевдонимы типов для лаконичного использования внедрения зависимостей в роутерах
BookServiceDep = Annotated[BookService, Depends(get_book_service)]
BookRepoDep = Annotated[BookRepository, Depends(get_book_repository)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
