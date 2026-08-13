"""
Модуль Pydantic-схем для валидации данных сущности Книги.
Определяет структуры данных для входящих запросов и исходящих ответов API.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """ Базовая схема книги, содержащая общие поля для всех операций """

    title: str = Field(..., min_length=1, max_length=500, description="Название книги")
    author: str = Field(..., min_length=1, max_length=300, description="Автор книги")
    year: int = Field(..., ge=0, description="Год издания")
    genre: str = Field(..., min_length=1, max_length=100, description="Жанр книги")
    pages: int = Field(..., gt=0, description="Количество страниц")
    isbn: str | None = Field(None, max_length=20, description="Уникальный номер ISBN")
    description: str | None = Field(None, description="Описание книги")
    extra: dict | None = Field(None, description="Дополнительные метаданные")


class BookCreate(BookBase):
    """ Схема для валидации данных при создании новой книги """

    pass


class BookUpdate(BaseModel):
    """ Схема для валидации данных при частичном обновлении книги """

    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=300)
    year: int | None = Field(None, ge=0)
    genre: str | None = Field(None, min_length=1, max_length=100)
    pages: int | None = Field(None, gt=0)
    available: bool | None = Field(None)
    isbn: str | None = Field(None, max_length=20)
    description: str | None = Field(None)
    extra: dict | None = Field(None)


class ShowBook(BookBase):
    """ Схема ответа API, возвращающая полные данные о книге из БД (DTO) """

    book_id: UUID = Field(..., description="Уникальный идентификатор книги")
    available: bool = Field(..., description="Статус доступности книги в библиотеке")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True # Позволяет Pydantic читать данные напрямую из ORM-моделей SQLAlchemy
    }
