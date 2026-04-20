from app.core.settings import Settings
from app.models.entities import User
from app.repositories.users import InMemoryUserRepository


class AuthService:
    """Authentication service. TODO: Implement registration, login, and user lookup."""
    
    def __init__(self, users: InMemoryUserRepository, settings: Settings) -> None:
        self.users = users
        self.settings = settings

    @staticmethod
    def _normalize_username(username: str) -> str:
        """Normalize username. TODO: Implement."""
        pass

    def register(self, username: str, password: str) -> User:
        """Register a new user. TODO: Implement."""
        pass

    def login(self, username: str, password: str) -> tuple[User, str]:
        """Authenticate user and return JWT token. TODO: Implement."""
        pass

    def get_by_id(self, user_id: str) -> User:
        """Get user by ID. TODO: Implement."""
        pass
