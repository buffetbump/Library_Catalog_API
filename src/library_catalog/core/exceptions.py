""" Модуль базовых инфраструктурных исключений приложения """

from typing import Any


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
