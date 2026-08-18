"""
Модуль общих Pydantic-схем для пагинации и проверки статуса приложения.
Определяет универсальные структуры для постраничных списков и ответов системы.
"""

from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """ Параметры для управления постраничным выводом списков данных """

    page: int = Field(1, ge=1, description="Номер страницы")
    page_size: int = Field(20, ge=1, le=100, description="Размер страницы")

    @property
    def offset(self) -> int:
        """ Вычисляет смещение строк для SQL-запроса к базе данных """

        return (self.page - 1) * self.page_size

    @property
    def  limit(self) -> int:
        """ Возвращает лимит количества строк для SQL-запроса """

        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """ Универсальная схема ответа для списков с поддержкой постраничной пагинации """

    items: list[T]
    total: int = Field(..., description="Всего элементов")
    page: int = Field(..., description="Текущая страница")
    page_size: int = Field(..., description="Размер страницы")
    pages: int = Field(..., description="Всего страниц")

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        pagination: PaginationParams,
    ) -> "PaginatedResponse[T]":
        """ Фабричный метод для автоматического расчета общего количества страниц """

        pages = (total + pagination.page_size - 1) // pagination.page_size

        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
        )


class HealthCheckResponse(BaseModel):
    """ Схема ответа для эндпоинта проверки технического состояния приложения """

    status: str = Field("healthy", description="Статус работоспособности веб-сервиса")
    database: str = Field("connected", description="Статус подключения к базе данных")
