from dataclasses import dataclass
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class User:
    id: str
    username: str
    password_hash: str
    created_at: datetime


@dataclass(slots=True)
class Drawing:
    id: str
    owner_id: str
    title: str
    file_name: str
    created_at: datetime
    updated_at: datetime
