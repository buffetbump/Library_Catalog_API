"""
Модуль базовой настройки стандартного логирования приложения.
"""

import logging
import sys


def setup_logging() -> None:
    """ Настраивает базовый формат и вывод логов в стандартный поток """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
