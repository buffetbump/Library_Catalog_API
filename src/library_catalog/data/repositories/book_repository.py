"""
Модуль репозитория для работы с сущностью Книги в базе данных.
Расширяет базовый репозиторий специфичными методами фильтрации и подсчета.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from library_catalog.data.models.book import Book
from library_catalog.data.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    """ Репозиторий для выполнения CRUD операций и фильтрации книг в PostgreSQL """

    def __init__(self, session: AsyncSession) -> None:
        """ Инициализирует репозиторий книги базовым классом и моделью Book """

        super().__init__(session, Book)

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """ Находит и возвращает книгу по её уникальному номеру ISBN """

        stmt = select(Book).where(Book.isbn == isbn)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> list[Book]:
        """
        Осуществляет поиск книг по комбинации фильтров с пагинацией.
        Для строк (название, автор) используется регистронезависимый поиск по подстроке.
        """

        stmt = select(Book)

        # Обработка None значений в фильтрах
        if title:
            stmt = stmt.where(Book.title.ilike(f"%{title}%"))
        if author:
            stmt = stmt.where(Book.author.ilike(f"%{author}%"))
        if genre:
            stmt = stmt.where(Book.genre == genre)
        if year is not None:
            stmt = stmt.where(Book.year == year)
        if available is not None:
            stmt = stmt.where(Book.available == available)

        # Добавляем лимиты для пагинации
        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
    ) -> int:
        """ Подсчитывает общее количество книг, подходящих под указанные фильтры """

        stmt = select(func.count()).select_from(Book)

        if title:
            stmt = stmt.where(Book.title.ilike(f"%{title}%"))
        if author:
            stmt = stmt.where(Book.author.ilike(f"%{author}%"))
        if genre:
            stmt = stmt.where(Book.genre == genre)
        if year is not None:
            stmt = stmt.where(Book.year == year)
        if available is not None:
            stmt = stmt.where(Book.available == available)

        result = await self.session.execute(stmt)
        return result.scalar_one() or 0
