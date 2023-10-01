from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.logger import logger

# from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
@version(1)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked

    booking_dict = SNewBooking.model_validate(booking).model_dump()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    logger.debug(f"{booking_dict=}")
    return booking_dict


@router.delete("/{booking_id}")
@version(1)
async def remove_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
