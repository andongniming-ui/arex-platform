from pydantic import BaseModel
from datetime import datetime
from typing import Any


class RepeaterConfigCreate(BaseModel):
    config_json: str
    plugins: list[str] | None = None
    sampling_rate: float = 1.0
    include_paths: list[str] | None = None
    exclude_paths: list[str] | None = None


class RepeaterConfigOut(BaseModel):
    id: str
    app_id: str
    config_json: str
    plugins: list[str] | None
    sampling_rate: float
    include_paths: list[str] | None
    exclude_paths: list[str] | None
    pushed_at: datetime | None
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionCreate(BaseModel):
    app_id: str
    name: str | None = None
    description: str | None = None
    created_by: str | None = None


class SessionOut(BaseModel):
    id: str
    app_id: str
    name: str | None
    description: str | None
    status: str
    started_at: datetime
    stopped_at: datetime | None
    record_count: int
    created_by: str | None
    error_message: str | None = None

    model_config = {"from_attributes": True}


class RecordingOut(BaseModel):
    id: str
    session_id: str
    app_id: str
    trace_id: str | None
    entry_type: str | None
    entry_app: str | None
    host: str | None
    path: str | None
    request_body: str | None
    response_body: str | None
    sub_invocations: list[Any] | None
    duration_ms: int | None
    timestamp: datetime | None
    tags: list[str] | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
