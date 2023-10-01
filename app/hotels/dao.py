from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT hotel_id, count(*) AS booked_rooms FROM bookings
            JOIN rooms ON rooms.id = bookings.room_id
            JOIN hotels ON hotels.id = rooms.hotel_id
            WHERE date_from <= '2023-06-20' AND date_to >= '2023-05-15'
            GROUP BY hotel_id
        )

            SELECT
                id, name, location, services, rooms_quantity,
                image_id, (rooms_quantity - COALESCE(booked_rooms, 0)) AS rooms_left
            FROM hotels
            LEFT JOIN booked_rooms ON hotels.id = booked_rooms.hotel_id
            WHERE hotels.location LIKE '%Алтай%'
        """
        booked_rooms = (
            select(Rooms.hotel_id, (func.count()).label("booked_rooms"))
            .select_from(Bookings)
            .join(Rooms, Rooms.id == Bookings.room_id)
            .join(Hotels, Hotels.id == Rooms.id)
            .where(
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from,
                )
            )
            .group_by(Rooms.hotel_id)
            .cte("booked_rooms")
        )
        """
            SELECT
                id, name, location, services, rooms_quantity,
                image_id, (rooms_quantity - COALESCE(booked_rooms, 0)) AS rooms_left
            FROM hotels
            LEFT JOIN booked_rooms ON hotels.id = booked_rooms.hotel_id
            WHERE hotels.location LIKE '%Алтай%'
        """
        get_available_hotels = (
            select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (
                    Hotels.rooms_quantity
                    - func.coalesce(booked_rooms.c.booked_rooms, 0)
                ).label("rooms_left"),
            )
            .select_from(Hotels)
            .join(booked_rooms, Hotels.id == booked_rooms.c.hotel_id, isouter=True)
            .filter(Hotels.location.ilike(f"%{location}%"))
        )
        # print(
        #     get_available_hotels.compile(engine, compile_kwargs={"literal_binds": True})
        # )
        async with async_session_maker() as session:
            result = await session.execute(get_available_hotels)
            return result.mappings().all()
