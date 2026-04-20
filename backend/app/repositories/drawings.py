from threading import Lock

from app.models.entities import Drawing


class InMemoryDrawingRepository:
    def __init__(self) -> None:
        self._items: dict[str, Drawing] = {}
        self._lock = Lock()

    def get_by_id(self, drawing_id: str) -> Drawing | None:
        return self._items.get(drawing_id)

    def list_all(self) -> list[Drawing]:
        return sorted(self._items.values(), key=lambda item: item.created_at, reverse=True)

    def list_by_owner(self, owner_id: str) -> list[Drawing]:
        return [item for item in self.list_all() if item.owner_id == owner_id]

    def create(self, drawing: Drawing) -> Drawing:
        with self._lock:
            if drawing.id in self._items:
                raise ValueError("Drawing already exists")
            self._items[drawing.id] = drawing
            return drawing

    def update(self, drawing: Drawing) -> Drawing:
        with self._lock:
            if drawing.id not in self._items:
                raise ValueError("Drawing not found")
            self._items[drawing.id] = drawing
            return drawing

    def delete(self, drawing_id: str) -> None:
        with self._lock:
            if drawing_id not in self._items:
                raise ValueError("Drawing not found")
            del self._items[drawing_id]
