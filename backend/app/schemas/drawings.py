from datetime import datetime

from pydantic import BaseModel


class DrawingResponse(BaseModel):
    id: str
    title: str
    owner_id: str
    owner_username: str
    created_at: datetime
    updated_at: datetime
    file_url: str
    can_edit: bool


class DrawingUploadResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    file_url: str
