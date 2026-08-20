"""
Интеграционные тесты для проверки взаимодействия слоев API, сервисов и базы данных.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_integration_crud_lifecycle(client: AsyncClient):
    """ Полный жизненный цикл книги через эндпоинты API (Create -> Read -> Update -> Delete) """

    # CREATE
    book_payload = {
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "year": 2002,
        "genre": "Programming",
        "pages": 240,
        "isbn": "9780321146533"
    }

    create_response = await client.post("/api/v1/books/", json=book_payload)
    assert create_response.status_code == 201
    created_book = create_response.json()
    book_id = created_book["book_id"]

    # READ
    get_response = await client.get(f"/api/v1/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json()["author"] == "Kent Beck"

    # UPDATE
    update_payload = {"title": "TDD Implemetation", "pages": 250}
    patch_response = await client.patch(f"/api/v1/books/{book_id}", json=update_payload)
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "TDD Implemetation"

    # DELETE
    delete_response = await client.delete(f"/api/v1/books/{book_id}")
    assert delete_response.status_code == 204

    # VERIFY DELETION
    final_get_response = await client.get(f"/api/v1/books/{book_id}")
    assert final_get_response.status_code == 404
