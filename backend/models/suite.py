import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class ReplaySuite(Base):
    """
    A suite groups multiple test cases and runs them in one shot.
    Useful for regression testing across a whole service.
    """
    __tablename__ = "replay_suite"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    # Ordered list of test-case IDs to execute
    case_ids: Mapped[list] = mapped_column(JSON, default=list)

    # Per-case target app override: {case_id: app_id}
    case_app_map: Mapped[dict | None] = mapped_column(JSON)

    # Default settings applied to every replay job spawned by this suite
    default_target_app_id: Mapped[str | None] = mapped_column(String(36))
    default_environment: Mapped[str | None] = mapped_column(String(64))
    default_override_host: Mapped[str | None] = mapped_column(String(256))
    default_concurrency: Mapped[int] = mapped_column(Integer, default=1)
    default_delay_ms: Mapped[int] = mapped_column(Integer, default=0)
    default_ignore_fields: Mapped[list | None] = mapped_column(JSON)
    default_diff_rules: Mapped[list | None] = mapped_column(JSON)
    default_assertions: Mapped[list | None] = mapped_column(JSON)
    default_perf_threshold_ms: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    runs: Mapped[list["SuiteRun"]] = relationship(
        "SuiteRun", back_populates="suite", cascade="all, delete-orphan",
        order_by="SuiteRun.created_at.desc()",
    )


class SuiteRun(Base):
    """
    One execution of a ReplaySuite — tracks aggregate results across all cases.
    """
    __tablename__ = "suite_run"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    suite_id: Mapped[str] = mapped_column(String(36), ForeignKey("replay_suite.id"), nullable=False)
    target_app_id: Mapped[str | None] = mapped_column(String(36))

    status: Mapped[str] = mapped_column(String(32), default="RUNNING")
    # RUNNING / DONE / FAILED

    total_cases: Mapped[int] = mapped_column(Integer, default=0)
    passed_cases: Mapped[int] = mapped_column(Integer, default=0)
    failed_cases: Mapped[int] = mapped_column(Integer, default=0)

    total_requests: Mapped[int] = mapped_column(Integer, default=0)
    passed_requests: Mapped[int] = mapped_column(Integer, default=0)
    overall_pass_rate: Mapped[float] = mapped_column(Float, default=0.0)

    job_ids: Mapped[list] = mapped_column(JSON, default=list)  # [replay_job_id, ...]

    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    suite: Mapped["ReplaySuite"] = relationship("ReplaySuite", back_populates="runs")
