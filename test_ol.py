""" Скрипт для ручной проверки интеграции с Open Library API """

import asyncio
from library_catalog.external.openlibrary.client import OpenLibraryClient


async def test():
    # Инициализируем клиент. Он сам подтянет настройки по умолчанию.
    client = OpenLibraryClient()
    print("🤖 Запуск ручной проверки сетевого слоя...")

    # Тест 1: Проверка точечного поиска по ISBN (Чистый код Мартина)
    data = await client.search_by_isbn("9780132350884")
    print(f"\n[ISBN Тест] Найдено: \n{data}")

    # Тест 2: Проверка поиска по названию и автору
    data = await client.search_by_title_author(
        "Clead Code",
        "Robert Martin"
    )
    print(f"\n[Название + Автор Тест] Найдено:\n{data}")

    # Обязательно закрываем пул сетевых соединений
    await client.close()

if __name__ == "__main__":
    asyncio.run(test())
