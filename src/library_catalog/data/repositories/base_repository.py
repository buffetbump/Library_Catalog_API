"""
Модуль базового обобщенного репозитория для CRUD операций.
Обеспечивает повторное использование стандартных запросов к базе данных.
"""

from typing import Generic, Type, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Объявляем переменную типа для типизации моделей
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """ Базовый класс, реализующий стандартные CRUD операции через SQLAlchemy """

    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        """ Инициализирует репозиторий асинхронной сессией и целевой моделью """

        self.session = session
        self.model = model

    async def create(self, **kwargs) -> T:
        """ Создает и сохраняет новую запись в базе данных """

        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: UUID) -> T | None:
        """ Возвращает запись по её первичному ключу (ID) """

        return await self.session.get(self.model, id)

    async def update(self, id: UUID, **kwargs) -> T | None:
        """ Обновляет существующую запись по её ID переданными параметрами """

        instance = await self.get_by_id(id)
        if instance is None:
            return None

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: UUID) -> bool:
        """ Удаляет запись из базы данных по её ID """

        instance = await self.get_by_id(id)
        if instance is None:
            return False

        await self.session.delete(instance)
        await self.session.commit()
        return True

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        """ Возвращает список всех записей с поддержкой пагинации """

        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
