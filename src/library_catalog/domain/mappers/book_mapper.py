"""
Модуль маппера для преобразования данных сущности Книги (Book entity в DTO).
Обеспечивает чистую конвертацию между ORM-моделями базы данных и Pydantic-схемами.
"""

from library_catalog.data.models.book import Book
from library_catalog.api.v1.schemas.book import ShowBook


class BookMapper:
    """ Класс-трансформатор для сущности Книги """

    @staticmethod
    def to_show_book(book: Book) -> ShowBook:
        """ 
        Преобразовать Book ORM модель в ShowBook DTO.
        
        Args:
            book: ORM модель из БД
            
        Returns:
            ShowBook: Pydantic модель для API
        """

        return ShowBook(
            book_id=book.book_id,
            title=book.title,
            author=book.author,
            year=book.year,
            genre=book.genre,
            pages=book.pages,
            available=book.available,
            isbn=book.isbn,
            description=book.description,
            extra=book.extra,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    @staticmethod
    def to_show_books(books: list[Book]) -> list[ShowBook]:
        """ Преобразовать список книг """

        return [BookMapper.to_show_book(book) for book in books]