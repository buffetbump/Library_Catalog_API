"""
Модуль конфигурации окружения Alembic для миграций базы данных.
Настроен для работы в асинхронном режиме с использованием SQLAlchemy 2.0.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импортируем конфигурацию приложения и базовую модель
from library_catalog.core.config import settings
from library_catalog.core.database import Base

# Импортируем модель Book, чтобы Alembic увидел таблицу books
from library_catalog.data.models import book


# Получаем объект конфигурации Alembic
config = context.config

# Автоматически подставляем URL базы данных из нашего файла настроек.
config.set_main_option(
    "sqlalchemy.url",
    str(settings.database_url)
)

# Настраиваем стандартное логирование Alembic, если файл конфигурации существует
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Передаем метаданные нашей Base модели для отслеживания изменений в таблицах
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """ Запуск миграций в 'offline' режиме (без реального подключения к БД) """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # проверяет не только наличие таблиц, но и типы колонок
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """ Вспомогательный метод для выполнения миграций внутри синхронного контекста """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """ Основной метод запуска миграций в 'online' режиме с асинхронным движком """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Передаем управление синхронному исполнителю миграций внутри асинхронной сессии
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """ Запуск миграций в 'online' режиме (с реальным подключением к БД) """

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
