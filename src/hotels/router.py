from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from exceptions import (CannotBookHotelForLongPeriod,
                        DateFromCannotBeAfterDateTo)
from hotels.dao import HotelDAO
from hotels.schemas import SHotelInfo

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> list[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    return await HotelDAO.find_all(location, date_from, date_to)
