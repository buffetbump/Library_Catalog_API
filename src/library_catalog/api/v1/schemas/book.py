"""
Модуль Pydantic-схем для валидации данных сущности Книги.
Определяет структуры данных для входящих запросов и исходящих ответов API.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    """ Базовая схема книги, содержащая общие поля для всех операций """

    title: str = Field(..., min_length=1, max_length=500, description="Название книги")
    author: str = Field(..., min_length=1, max_length=300, description="Автор книги")
    year: int = Field(..., ge=1000, le=2100, description="Год издания")
    genre: str = Field(..., min_length=1, max_length=100, description="Жанр книги")
    pages: int = Field(..., gt=0, description="Количество страниц")


class BookCreate(BookBase):
    """ Схема для валидации данных при создании новой книги """

    isbn: str | None = Field(None, min_length=10, max_length=20, description="Уникальный номер ISBN")
    description: str | None = Field(None, max_length=5000, description="Описание книги")

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        """ Очищает ISBN от лишних символов и проверяет корректность длины """

        if v is None:
            return v

        # Удаляем дефисы и пробелы для стандартизации формата хранения
        clean = v.replace("-", "").replace(" ", "")

        # Проверить что только цифры (и X для ISBN-10)
        if not clean.replace("X", "").isdigit():
            raise ValueError("ISBN должен содержать только цифры")

        # Проверить длину ISBN
        if len(clean) not in (10, 13):
            raise ValueError("ISBN должен состоять из 10 или 13 цифр")

        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Clean Code",
                    "author": "Robert Martin",
                    "year": 2008,
                    "genre": "Programming",
                    "pages": 464,
                    "isbn": "978-0132350884",
                    "description": "A Handbook of Agile Software Craftsmanship"
                }
            ]
        }
    }


class BookUpdate(BaseModel):
    """ Схема для валидации данных при частичном обновлении книги """

    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=300)
    year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, min_length=1, max_length=100)
    pages: int | None = Field(None, gt=0)
    available: bool | None = Field(None)
    isbn: str | None = Field(None, max_length=20)
    description: str | None = Field(None)


class ShowBook(BookBase):
    """ Схема ответа API, возвращающая полные данные о книге из БД (DTO) """

    book_id: UUID = Field(..., description="Уникальный идентификатор книги")
    available: bool = Field(..., description="Статус доступности книги в библиотеке")
    isbn : str | None = Field(None, description="Уникальный номер ISBN")
    description: str | None = Field(None, description="Описание книги")
    extra: dict | None = Field(None, description="Дополнительные метаданные")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True, # Позволяет Pydantic читать данные напрямую из ORM-моделей SQLAlchemy
        "json_schema_extra": {
            "examples": [
                {
                    "book_id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Clean Code",
                    "author": "Robert Martin",
                    "year": 2008,
                    "genre": "Programming",
                    "pages": 464,
                    "available": True,
                    "isbn": "978-0132350884",
                    "description": "A Handbook of Agile Software Craftsmanship",
                    "extra": {
                        "cover_url": "https://covers.openlibrary.org/b/id/123-L.jpg",
                        "subjects": ["Computer Science", "Software Engineering"]
                    },
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-01T12:00:00"
                }
            ]
        }
    }


class BookFilters(BaseModel):
    """ Схема для фильтрации поисковых запросов в каталоге """

    title: str | None = Field(None, description="Поиск по названию (частичное совпадение)")
    author: str | None = Field(None, description="Поиск по автору (частичное совпадение)")
    genre: str | None = Field(None, description="Точное совпадение жанра")
    year: int | None = Field(None, description="Точное совпадение года")
    available: bool | None = Field(None, description="Фильтр по доступности")
