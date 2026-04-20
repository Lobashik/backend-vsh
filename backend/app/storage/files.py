from pathlib import Path


class DrawingFileStorage:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, drawing_id: str) -> Path:
        return self.base_dir / f"{drawing_id}.png"

    def save_png(self, drawing_id: str, content: bytes) -> Path:
        file_path = self.path_for(drawing_id)
        with file_path.open("wb") as f:
            f.write(content)
        return file_path

    def delete_png(self, drawing_id: str) -> None:
        file_path = self.path_for(drawing_id)
        if file_path.exists():
            file_path.unlink()
