from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.dependencies import get_auth_service, map_app_error, to_user_read
from app.core.errors import AppError
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserRead:
    try:
        user = auth_service.register(payload.username, payload.password)
    except AppError as error:
        raise map_app_error(error)
    return to_user_read(user)


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    try:
        _, token = auth_service.login(payload.username, payload.password)
    except AppError as error:
        raise map_app_error(error)
    return TokenResponse(access_token=token)
