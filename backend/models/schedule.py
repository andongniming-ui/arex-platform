import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class ScheduledReplay(Base):
    __tablename__ = "scheduled_replay"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_case.id"), nullable=False)
    target_app_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)

    cron_expr: Mapped[str] = mapped_column(String(64), nullable=False)
    # Standard 5-field cron: "minute hour day month weekday"
    # Examples: "0 2 * * *" (daily 2am), "0 9 * * 1-5" (weekdays 9am)

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    concurrency: Mapped[int] = mapped_column(Integer, default=1)
    delay_ms: Mapped[int] = mapped_column(Integer, default=0)
    ignore_fields: Mapped[list | None] = mapped_column(JSON)
    diff_rules: Mapped[list | None] = mapped_column(JSON)
    assertions: Mapped[list | None] = mapped_column(JSON)
    perf_threshold_ms: Mapped[int | None] = mapped_column(Integer)
    override_host: Mapped[str | None] = mapped_column(String(256))
    environment: Mapped[str | None] = mapped_column(String(64))
    webhook_url: Mapped[str | None] = mapped_column(String(512))
    notify_type: Mapped[str | None] = mapped_column(String(32))  # generic / dingtalk / wecom

    last_run_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_job_id: Mapped[str | None] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
