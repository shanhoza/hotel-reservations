import pytest

from app.hotels.dao import HotelDAO


@pytest.mark.parametrize(
    "hotel_id,exists",
    [
        (1, True),
        (6, True),
        (7, False),
    ],
)
async def test_find_hotel_by_id(hotel_id, exists):
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)

    if exists:
        assert hotel
        assert hotel["id"] == hotel_id
    else:
        assert not hotel
