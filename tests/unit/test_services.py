"""
Юнит-тесты для проверки изолированной бизнес-логики доменных сервисов.
"""

import pytest

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from library_catalog.domain.services.book_service import BookService
from library_catalog.api.v1.schemas.book import BookCreate
from library_catalog.domain.exceptions import BookAlreadyExistsException, BookNotFoundException


@pytest.mark.asyncio
async def test_create_book_already_exists_raises_exception():
    """ Сервис должен выбросить исключение, если книга с таким ISBN уже есть """

    mock_repo = MagicMock()
    mock_repo.find_by_isbn = AsyncMock(return_value=MagicMock())
    mock_client = MagicMock()

    service = BookService(book_repository=mock_repo, openlibrary_client=mock_client)
    book_data = BookCreate(title="Test", author="Test", description="Test", year=2020, genre="IT", pages=100, isbn="1234567890")

    with pytest.raises(BookAlreadyExistsException):
        await service.create_book(book_data)


@pytest.mark.asyncio
async def test_get_book_not_found_raises_exception():
    """ Сервис должен выбросить исключение, если книга не найдена по ID """

    mock_repo = MagicMock()
    mock_repo.get_by_id = AsyncMock(return_value=None)
    mock_client = MagicMock()

    service = BookService(book_repository=mock_repo, openlibrary_client=mock_client)

    with pytest.raises(BookNotFoundException):
        await service.get_book(uuid4())
