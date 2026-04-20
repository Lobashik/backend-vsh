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
    pass


@router.post("", response_model=DrawingUploadResponse, status_code=201)
async def create_image(
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
) -> DrawingUploadResponse:
    pass

@router.get("/{drawing_id}", response_model=DrawingResponse)
def get_my_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> DrawingResponse:
    pass


@router.get("/{drawing_id}/file")
def get_image_file(
    drawing_id: str,
    _current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
):
    pass


@router.patch("/{drawing_id}", response_model=DrawingUploadResponse)
async def update_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
    title: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
) -> DrawingUploadResponse:
    pass


@router.delete("/{drawing_id}")
def delete_image(
    drawing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> dict[str, str]:
    pass
