""" Модуль базовых инфраструктурных исключений приложения """

from typing import Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """ Базовое исключение для всего приложения """

    def __init__(self, message: str, status_code: int = 400) -> None:
        """ Инциализирует ошибку сообщением и HTTP-статусом """

        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    """ Исключение для ситуаций, когда ресурс не найден (404 Not Found) """

    def __init__(self, resource: str, identifier: Any) -> None:
        """ Формирует стандартное англоязычное сообщение о ненахождении ресурса """

        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message=message, status_code=404)


def register_exception_handlers(app: FastAPI) -> None:
    """ Регистрирует глобальные обработчики кастомных исключений в FastAPI """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
