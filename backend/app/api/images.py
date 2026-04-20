from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse

from app.dependencies.dependencies import get_current_user, get_drawings_service, map_app_error
from app.core.errors import AppError, ValidationError
from app.models.entities import User
from app.schemas.drawings import DrawingResponse, DrawingUploadResponse
from app.services.drawings import DrawingsService

router = APIRouter(prefix="/images", tags=["images"])


def _to_response(item) -> DrawingResponse:
    return DrawingResponse(
        id=item.id,
        title=item.title,
        owner_id=item.owner_id,
        owner_username=item.owner_username,
        created_at=item.created_at,
        updated_at=item.updated_at,
        file_url=item.file_url,
        can_edit=item.can_edit,
    )


@router.get("", response_model=list[DrawingResponse])
def list_my_images(
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> list[DrawingResponse]:
    return [_to_response(item) for item in drawings_service.list_mine(current_user)]


@router.post("", response_model=DrawingUploadResponse, status_code=201)
async def create_image(
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
) -> DrawingUploadResponse:
    content = await file.read()
    try:
        created = drawings_service.create(current_user, title, content, file.content_type)
    except AppError as error:
        raise map_app_error(error)
    return DrawingUploadResponse(
        id=created.id,
        title=created.title,
        created_at=created.created_at,
        updated_at=created.updated_at,
        file_url=created.file_url,
    )


@router.get("/{drawing_id}", response_model=DrawingResponse)
def get_my_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> DrawingResponse:
    try:
        return _to_response(drawings_service.get_mine(drawing_id, current_user))
    except AppError as error:
        raise map_app_error(error)


@router.get("/{drawing_id}/file")
def get_image_file(
    drawing_id: str,
    _current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
):
    try:
        path = drawings_service.file_path(drawing_id)
    except AppError as error:
        raise map_app_error(error)
    return FileResponse(path, media_type="image/png", filename=f"{drawing_id}.png")


@router.patch("/{drawing_id}", response_model=DrawingUploadResponse)
async def update_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
    title: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
) -> DrawingUploadResponse:
    if file is None:
        raise map_app_error(ValidationError("File is required"))
    content = await file.read()
    try:
        updated = drawings_service.update(drawing_id, current_user, title, content, file.content_type)
    except AppError as error:
        raise map_app_error(error)
    return DrawingUploadResponse(
        id=updated.id,
        title=updated.title,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
        file_url=updated.file_url,
    )


@router.delete("/{drawing_id}")
def delete_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> dict[str, str]:
    try:
        drawings_service.delete(drawing_id, current_user)
    except AppError as error:
        raise map_app_error(error)
    return {"detail": "Drawing deleted"}
