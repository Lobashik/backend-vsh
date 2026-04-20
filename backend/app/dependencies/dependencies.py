from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.errors import AppError, ConflictError, NotFoundError, PermissionDeniedError, ValidationError
from app.core.security import SecurityError, decode_access_token
from app.core.settings import get_settings
from app.models.entities import User
from app.repositories.drawings import InMemoryDrawingRepository
from app.repositories.users import InMemoryUserRepository
from app.schemas.auth import UserRead
from app.services.auth import AuthService
from app.services.drawings import DrawingsService
from app.storage.files import DrawingFileStorage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@lru_cache(maxsize=1)
def get_user_repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@lru_cache(maxsize=1)
def get_drawings_repo() -> InMemoryDrawingRepository:
    return InMemoryDrawingRepository()


@lru_cache(maxsize=1)
def get_file_storage() -> DrawingFileStorage:
    settings = get_settings()
    return DrawingFileStorage(Path(settings.storage_dir))


@lru_cache(maxsize=1)
def get_auth_service() -> AuthService:
    return AuthService(get_user_repo(), get_settings())


@lru_cache(maxsize=1)
def get_drawings_service() -> DrawingsService:
    return DrawingsService(get_drawings_repo(), get_user_repo(), get_file_storage())


def map_app_error(error: AppError) -> HTTPException:
    if isinstance(error, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    if isinstance(error, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    if isinstance(error, PermissionDeniedError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))
    if isinstance(error, ValidationError):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """TODO: Implement JWT token validation and user retrieval."""
    pass


def to_user_read(user: User) -> UserRead:
    return UserRead(id=user.id, username=user.username, created_at=user.created_at)
