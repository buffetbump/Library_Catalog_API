"""
Модуль доменных исключений для сущности Книги. 
Определяет все специфичные ошибки бизнес-логики для каталога книг.
"""

from uuid import UUID
from library_catalog.core.exceptions import AppException, NotFoundException


class BookNotFoundException(NotFoundException):
    """ Исключение, когда книга не найдена в базе данных """

    def __init__(self, book_id: UUID) -> None:
        """ Передаем параметры в NotFoundException для формирования ответа 404 """

        super().__init__(resource="Book", identifier=book_id)


class BookAlreadyExistsException(AppException):
    """ Исключение, если книга с таким ISBN уже существует """

    def __init__(self, isbn: str) -> None:
        """ Формирует ошибку с кодом 409 Conflict """

        super().__init__(
            message=f"Book with ISBN '{isbn}' already exists",
            status_code=409,
        )


class InvalidYearException(AppException):
    """ Исключение для некорреткного года издания книги """

    def __init__(self, year: int) -> None:
        """ Формирует ошибку с кодом 404 Bad Request """

        super().__init__(
            message=f"Year {year} is invalid. It cannot be in the future",
            status_code=400,
        )


class InvalidPagesException(AppException):
    """ Исключение для некорреткного количества страниц """

    def __init__(self, pages: int) -> None:
        """ Формирует ошибку со статусом 400 Bad Request """

        super().__init__(
            message=f"Page count {pages} is invalid. Book must have at least 1 page.",
            status_code=400,
        )


class OpenLibraryException(AppException):
    """ Исключение при общих ошибках интеграции со сторонним сервисом Open Library API """

    def __init__(self, details: str) -> None:
        """ Формирует ошибку внешнего сервиса со статусом 502 Bad Gateway """

        super().__init__(
            message=f"External Open Library API error: {details}",
            status_code=502,
        )


class OpenLibraryTimeoutException(AppException):
    """ Исключение при превышении времени ожидания от Open Library API """

    def __init__(self) -> None:
        """ Формирует ошибку таймаута внешнего сервиса со статусом 504 Bad Gateway Timeout """

        super().__init__(
            message="Connection to Open Library API timed out",
            status_code=504,
        )
