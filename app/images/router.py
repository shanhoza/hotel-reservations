import shutil

from fastapi import APIRouter, UploadFile, status

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/hotels", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
