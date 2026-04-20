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
        return [self._view(item, True) for item in self.drawings.list_by_owner(user.id)]

    def list_gallery(self) -> list[DrawingView]:
        return [self._view(item, False) for item in self.drawings.list_all()]

    def get_mine(self, drawing_id: str, user: User) -> DrawingView:
        item = self.drawings.get_by_id(drawing_id)
        if item is None:
            raise NotFoundError("Drawing not found")
        if item.owner_id != user.id:
            raise PermissionDeniedError("You do not have access to this drawing")
        return self._view(item, True)

    def create(self, user: User, title: str, content: bytes, content_type: str | None) -> DrawingView:
        self._validate_png(content_type, content)
        drawing_id = str(uuid4())
        item = Drawing(
            id=drawing_id,
            owner_id=user.id,
            title=self._validate_title(title),
            file_name=f"{drawing_id}.png",
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.file_storage.save_png(drawing_id, content)
        try:
            self.drawings.create(item)
        except Exception as exc:
            self.file_storage.delete_png(drawing_id)
            raise ConflictError("Failed to persist drawing") from exc
        return self._view(item, True)

    def update(
        self,
        drawing_id: str,
        user: User,
        title: str | None,
        content: bytes,
        content_type: str | None,
    ) -> DrawingView:
        existing = self.drawings.get_by_id(drawing_id)
        if existing is None:
            raise NotFoundError("Drawing not found")
        if existing.owner_id != user.id:
            raise PermissionDeniedError("You do not have access to this drawing")

        self._validate_png(content_type, content)
        updated = Drawing(
            id=existing.id,
            owner_id=existing.owner_id,
            title=self._validate_title(title) if title is not None else existing.title,
            file_name=existing.file_name,
            created_at=existing.created_at,
            updated_at=utc_now(),
        )
        self.file_storage.save_png(drawing_id, content)
        self.drawings.update(updated)
        return self._view(updated, True)

    def delete(self, drawing_id: str, user: User) -> None:
        existing = self.drawings.get_by_id(drawing_id)
        if existing is None:
            raise NotFoundError("Drawing not found")
        if existing.owner_id != user.id:
            raise PermissionDeniedError("You do not have access to this drawing")
        self.drawings.delete(drawing_id)
        self.file_storage.delete_png(drawing_id)

    def file_path(self, drawing_id: str) -> str:
        if self.drawings.get_by_id(drawing_id) is None:
            raise NotFoundError("Drawing not found")
        path = self.file_storage.path_for(drawing_id)
        if not path.exists():
            raise NotFoundError("Drawing file not found")
        return str(path)
