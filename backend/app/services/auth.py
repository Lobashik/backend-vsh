from uuid import uuid4

from app.core.errors import ConflictError, PermissionDeniedError, ValidationError
from app.core.security import create_access_token, hash_password, verify_password
from app.core.settings import Settings
from app.models.entities import User, utc_now
from app.repositories.users import InMemoryUserRepository


class AuthService:
    def __init__(self, users: InMemoryUserRepository, settings: Settings) -> None:
        self.users = users
        self.settings = settings

    @staticmethod
    def _normalize_username(username: str) -> str:
        return username.strip()

    def register(self, username: str, password: str) -> User:
        normalized = self._normalize_username(username)
        if not normalized:
            raise ValidationError("Username is required")
        if self.users.get_by_username(normalized):
            raise ConflictError("User with this username already exists")
        user = User(
            id=str(uuid4()),
            username=normalized,
            password_hash=hash_password(password),
            created_at=utc_now(),
        )
        return self.users.create(user)

    def login(self, username: str, password: str) -> tuple[User, str]:
        normalized = self._normalize_username(username)
        user = self.users.get_by_username(normalized)
        if user is None or not verify_password(password, user.password_hash):
            raise PermissionDeniedError("Invalid username or password")
        token = create_access_token(user.id, self.settings, {"username": user.username})
        return user, token

    def get_by_id(self, user_id: str) -> User:
        user = self.users.get_by_id(user_id)
        if user is None:
            raise PermissionDeniedError("Authenticated user not found")
        return user
