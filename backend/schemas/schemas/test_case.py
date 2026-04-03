from pydantic import BaseModel
from datetime import datetime


class TestCaseCreate(BaseModel):
    name: str
    description: str | None = None
    app_id: str | None = None
    tags: list[str] | None = None
    created_by: str | None = None


class TestCaseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    app_id: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class TestCaseOut(BaseModel):
    id: str
    name: str
    description: str | None
    app_id: str | None
    tags: list[str] | None
    status: str
    recording_count: int
    created_by: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddRecordingsRequest(BaseModel):
    recording_ids: list[str]
