from threading import Lock

from app.models.entities import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._items: dict[str, User] = {}
        self._lock = Lock()

    def get_by_id(self, user_id: str) -> User | None:
        return self._items.get(user_id)

    def get_by_username(self, username: str) -> User | None:
        normalized = username.casefold()
        return next((item for item in self._items.values() if item.username.casefold() == normalized), None)

    def create(self, user: User) -> User:
        with self._lock:
            if self.get_by_username(user.username):
                raise ValueError("User already exists")
            self._items[user.id] = user
            return user
