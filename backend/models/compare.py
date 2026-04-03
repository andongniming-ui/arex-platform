import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class CompareRun(Base):
    """
    A/B environment comparison: replay the same test case against two apps
    and compare their responses against each other and against the original recording.
    """
    __tablename__ = "compare_run"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str | None] = mapped_column(String(256))
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_case.id"), nullable=False)
    app_a_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)
    app_b_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)

    status: Mapped[str] = mapped_column(String(32), default="RUNNING")
    # RUNNING / DONE / FAILED

    ignore_fields: Mapped[list | None] = mapped_column(JSON)
    diff_rules: Mapped[list | None] = mapped_column(JSON)

    total_count: Mapped[int] = mapped_column(Integer, default=0)
    # How many recordings had same verdict in both environments (both PASS or both FAIL)
    agreed_count: Mapped[int] = mapped_column(Integer, default=0)
    # How many recordings had different verdicts between the two environments
    diverged_count: Mapped[int] = mapped_column(Integer, default=0)

    def __init__(self, **kwargs):
        kwargs.setdefault("total_count", 0)
        kwargs.setdefault("agreed_count", 0)
        kwargs.setdefault("diverged_count", 0)
        super().__init__(**kwargs)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

    results: Mapped[list["CompareResult"]] = relationship(
        "CompareResult", back_populates="run", cascade="all, delete-orphan",
    )


class CompareResult(Base):
    __tablename__ = "compare_result"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("compare_run.id"), nullable=False)
    recording_id: Mapped[str] = mapped_column(String(36), ForeignKey("recording.id"), nullable=False)

    path: Mapped[str | None] = mapped_column(String(1024))
    entry_type: Mapped[str | None] = mapped_column(String(32))

    # App A results
    status_a: Mapped[str | None] = mapped_column(String(32))
    resp_a: Mapped[str | None] = mapped_column(Text)
    diff_score_a: Mapped[float | None] = mapped_column(Float)  # vs original
    duration_a_ms: Mapped[int | None] = mapped_column(Integer)

    # App B results
    status_b: Mapped[str | None] = mapped_column(String(32))
    resp_b: Mapped[str | None] = mapped_column(Text)
    diff_score_b: Mapped[float | None] = mapped_column(Float)  # vs original
    duration_b_ms: Mapped[int | None] = mapped_column(Integer)

    # Direct A vs B comparison
    diff_a_vs_b: Mapped[str | None] = mapped_column(Text)
    diff_score_a_vs_b: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    run: Mapped["CompareRun"] = relationship("CompareRun", back_populates="results")
