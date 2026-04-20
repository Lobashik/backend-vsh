from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.dependencies.dependencies import get_current_user, to_user_read
from app.models.entities import User
from app.schemas.auth import UserRead

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserRead)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    return to_user_read(current_user)
