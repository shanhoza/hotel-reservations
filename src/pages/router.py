from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time),
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels,
        },
    )
