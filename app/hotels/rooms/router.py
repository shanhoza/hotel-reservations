from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo

router = APIRouter(
    prefix="/rooms",
    tags=["Номера отелей"],
)


@router.get("/{hotel_id}")
# нужно кэшировать
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> list[SRoomInfo]:
    return await RoomDAO.find_all(hotel_id, date_from, date_to)
