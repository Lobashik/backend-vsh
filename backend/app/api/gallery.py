from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.dependencies.dependencies import get_current_user, get_drawings_service
from app.models.entities import User
from app.schemas.drawings import DrawingResponse
from app.services.drawings import DrawingsService

router = APIRouter(tags=["gallery"])


def _to_response(item) -> DrawingResponse:
    return DrawingResponse(
        id=item.id,
        title=item.title,
        owner_id=item.owner_id,
        owner_username=item.owner_username,
        created_at=item.created_at,
        updated_at=item.updated_at,
        file_url=item.file_url,
        can_edit=False,
    )


@router.get("/gallery", response_model=list[DrawingResponse])
def gallery(
    _current_user: Annotated[User, Depends(get_current_user)],
    drawings_service: Annotated[DrawingsService, Depends(get_drawings_service)],
) -> list[DrawingResponse]:
    return [_to_response(item) for item in drawings_service.list_gallery()]
