"""
Точка входа FastAPI приложения Library Catalog.
Координирует жизненный цикл, подключает middleware, обработчики ошибок и роутеры.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from library_catalog.core.config import settings
from library_catalog.core.database import dispose_engine
from library_catalog.core.exceptions import register_exception_handlers
from library_catalog.core.logging_config import setup_logging
from library_catalog.api.v1.routers import books, health


# ========== LIFECYCLE EVENTS ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ 
    Управляет событиями запуска и остановки приложения 
    
    Выполняется при:
    - startup: настройка логирования
    - shutdown: закрытие подключений к БД
    """

    # Выполняется при старте веб-сервера
    setup_logging()
    print("🚀 Application started")

    yield

    # Выполняется при корректной остановке веб-сервера
    await dispose_engine()
    print("👋 Application stopped")


# ========== CREATE APP ==========

app = FastAPI(
    title=settings.app_name,
    description="REST API для управления библиотечным каталогом",
    version="1.0.0",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan,
)

# ========== MIDDLEWARE ==========

# Настраиваем CORS политики для безопасных запросов из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== EXCEPTION HANDLERS ==========

register_exception_handlers(app)

# ========== ROUTERS ==========

# Подключаем роутеры первой версии API каталога
app.include_router(
    books.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    health.router,
    prefix=settings.api_v1_prefix,
)

# ========== ROOT ENDPOINT ==========

@app.get("/", summary="Корневой эндпоинт")
async def root():
    """ Приветственное сообщение со ссылкой на документацию """

    return {
        "message": "Welcome to Library Catalog API",
        "docs": settings.docs_url,
        "version": "1.0.0",
    }

# ========== RUN ==========

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
