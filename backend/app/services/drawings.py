from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.core.errors import ConflictError, NotFoundError, PermissionDeniedError, ValidationError
from app.core.settings import get_settings
from app.models.entities import Drawing, User, utc_now
from app.repositories.drawings import InMemoryDrawingRepository
from app.repositories.users import InMemoryUserRepository
from app.storage.files import DrawingFileStorage


@dataclass(slots=True)
class DrawingView:
    id: str
    title: str
    owner_id: str
    owner_username: str
    created_at: datetime
    updated_at: datetime
    file_url: str
    can_edit: bool


class DrawingsService:
    def __init__(
        self,
        drawings: InMemoryDrawingRepository,
        users: InMemoryUserRepository,
        file_storage: DrawingFileStorage,
    ) -> None:
        self.drawings = drawings
        self.users = users
        self.file_storage = file_storage
        self.settings = get_settings()

    @staticmethod
    def _validate_title(title: str) -> str:
        normalized = title.strip()
        if not normalized:
            raise ValidationError("Title is required")
        if len(normalized) > 120:
            raise ValidationError("Title is too long")
        return normalized

    @staticmethod
    def _validate_png(content_type: str | None, content: bytes) -> None:
        if content_type not in {"image/png", "application/octet-stream", None}:
            raise ValidationError("Only PNG uploads are supported")
        if len(content) < 8 or content[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValidationError("Uploaded file is not a valid PNG image")

    def _owner_name(self, owner_id: str) -> str:
        owner = self.users.get_by_id(owner_id)
        if owner is None:
            raise NotFoundError("Owner not found")
        return owner.username

    def _view(self, drawing: Drawing, can_edit: bool) -> DrawingView:
        file_url = f"{self.settings.api_prefix}/images/{drawing.id}/file"
        return DrawingView(
            id=drawing.id,
            title=drawing.title,
            owner_id=drawing.owner_id,
            owner_username=self._owner_name(drawing.owner_id),
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
            file_url=file_url,
            can_edit=can_edit,
        )

    def list_mine(self, user: User) -> list[DrawingView]:
        pass

    def list_gallery(self) -> list[DrawingView]:
        pass

    def get_mine(self, drawing_id: str, user: User) -> DrawingView:
        pass

    def create(self, user: User, title: str, content: bytes, content_type: str | None) -> DrawingView:
        pass

    def update(
        self,
        drawing_id: str,
        user: User,
        title: str | None,
        content: bytes,
        content_type: str | None,
    ) -> DrawingView:
        pass

    def delete(self, drawing_id: str, user: User) -> None:
        pass

    def file_path(self, drawing_id: str) -> str:
        pass
