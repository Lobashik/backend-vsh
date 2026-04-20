from typing import Any

from app.core.settings import Settings


class SecurityError(ValueError):
    pass


def hash_password(password: str) -> str:
    """Hash a plain text password. TODO: Implement with passlib."""
    pass


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain text password against its hash. TODO: Implement with passlib."""
    pass


def create_access_token(subject: str, settings: Settings, extra_claims: dict[str, Any] | None = None) -> str:
    """Create a JWT access token. TODO: Implement with python-jose."""
    pass


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    """Decode and validate a JWT access token. TODO: Implement with python-jose."""
    pass
