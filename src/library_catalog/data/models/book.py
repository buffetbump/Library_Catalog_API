"""
Модуль декларативной ORM-модели Книги для базы данных.
Описывает структуру таблицы 'books' с использованием синтаксиса SQLAlchemy 2.0.
"""

import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from library_catalog.core.database import Base


class Book(Base):
    """
    ORM-модель, представляющая книгу в библиотечном каталоге.
    Содержит информацию о названии, авторе, годе издания, жанре,
    количестве страниц, уникальном номере ISBN и дополнительных метаданных.
    """

    __tablename__ = "books"

    # Обязательные поля
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True
    )

    author: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index=True,
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    genre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    pages: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    # Опциональные поля
    isbn: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    extra: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # Временные метки (Timestamps)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """ Возвращает строковое представление объекта книги для логов """

        return f"<Book(id={self.book_id}, title='{self.title}')>"
