import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """фикстура - функция подготовки среды для тестирования
    (подъем/наполнение БД, возвращать частоиспользуемые данные,
    могут отдавать временные сессии через yield)"""
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in (
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings),
        ):
            query = insert(Model).values(values)
            await session.execute(query)
        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "test",
            },
        )
        assert ac.cookies["booking_access_token"]
        yield ac
