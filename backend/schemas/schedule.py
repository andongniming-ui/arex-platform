from pydantic import BaseModel
from datetime import datetime


class ScheduleCreate(BaseModel):
    name: str
    case_id: str
    target_app_id: str
    cron_expr: str
    enabled: bool = True
    concurrency: int = 1
    delay_ms: int = 0
    override_host: str | None = None
    environment: str | None = None
    ignore_fields: list[str] | None = None
    diff_rules: list[dict] | None = None
    assertions: list[dict] | None = None
    perf_threshold_ms: int | None = None
    webhook_url: str | None = None
    notify_type: str | None = None  # generic / dingtalk / wecom


class ScheduleUpdate(BaseModel):
    name: str | None = None
    cron_expr: str | None = None
    enabled: bool | None = None
    concurrency: int | None = None
    delay_ms: int | None = None
    override_host: str | None = None
    environment: str | None = None
    ignore_fields: list[str] | None = None
    diff_rules: list[dict] | None = None
    assertions: list[dict] | None = None
    perf_threshold_ms: int | None = None
    webhook_url: str | None = None
    notify_type: str | None = None


class ScheduleOut(BaseModel):
    id: str
    name: str
    case_id: str
    target_app_id: str
    cron_expr: str
    enabled: bool
    concurrency: int
    delay_ms: int
    override_host: str | None
    environment: str | None
    ignore_fields: list[str] | None
    diff_rules: list[dict] | None
    assertions: list[dict] | None
    perf_threshold_ms: int | None
    webhook_url: str | None
    notify_type: str | None
    last_run_at: datetime | None
    last_job_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
