import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class ReplayJob(Base):
    __tablename__ = "replay_job"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_case.id"), nullable=False)
    target_app_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("application.id"), nullable=False
    )
    environment: Mapped[str | None] = mapped_column(String(64))

    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    # PENDING / RUNNING / DONE / FAILED / CANCELLED

    total_count: Mapped[int] = mapped_column(Integer, default=0)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    fail_count: Mapped[int] = mapped_column(Integer, default=0)

    concurrency: Mapped[int] = mapped_column(Integer, default=1)
    delay_ms: Mapped[int] = mapped_column(Integer, default=0)
    override_host: Mapped[str | None] = mapped_column(String(256))
    ignore_fields: Mapped[list | None] = mapped_column(JSON)  # e.g. ["timestamp","requestId"]
    diff_rules: Mapped[list | None] = mapped_column(JSON)     # Smart Diff Rules
    assertions: Mapped[list | None] = mapped_column(JSON)     # Assertion Rules
    perf_threshold_ms: Mapped[int | None] = mapped_column(Integer)  # Flag results exceeding this latency
    use_sub_invocation_mocks: Mapped[bool] = mapped_column(default=False)  # Mock DB/RPC sub-calls via Repeater agent
    webhook_url: Mapped[str | None] = mapped_column(String(512))
    notify_type: Mapped[str | None] = mapped_column(String(32))  # generic / dingtalk / wecom

    # P0: 智能降噪
    smart_noise_reduction: Mapped[bool] = mapped_column(default=False)  # 启用内置智能降噪规则
    # P0: 流量放大
    repeat_count: Mapped[int] = mapped_column(Integer, default=1)  # 每条录制回放次数
    # P1: 请求头转换
    header_transforms: Mapped[list | None] = mapped_column(JSON)  # [{"type": "replace", "key": "Host", "value": "..."}]
    # P1: 失败重试
    retry_count: Mapped[int] = mapped_column(Integer, default=0)  # 失败重试次数

    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_by: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test_case: Mapped["TestCase"] = relationship("TestCase", back_populates="replay_jobs")
    target_app: Mapped["Application"] = relationship("Application", foreign_keys=[target_app_id])
    results: Mapped[list["ReplayResult"]] = relationship(
        "ReplayResult", back_populates="job", cascade="all, delete-orphan"
    )


class ReplayResult(Base):
    __tablename__ = "replay_result"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("replay_job.id"), nullable=False)
    recording_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("recording.id"), nullable=False
    )

    status: Mapped[str | None] = mapped_column(String(32))
    # PASS / FAIL / ERROR / IGNORED

    original_response: Mapped[str | None] = mapped_column(Text)
    replayed_response: Mapped[str | None] = mapped_column(Text)
    diff_json: Mapped[str | None] = mapped_column(Text)
    diff_score: Mapped[float | None] = mapped_column(Float)
    error_message: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    replayed_status_code: Mapped[int | None] = mapped_column(Integer)
    assertion_results: Mapped[list | None] = mapped_column(JSON)  # [{type, passed, message}]
    replayed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Failure analysis fields
    failure_category: Mapped[str | None] = mapped_column(String(32))
    # ENVIRONMENT / DATA_ISSUE / BUG / PERFORMANCE / UNKNOWN
    failure_reason: Mapped[str | None] = mapped_column(Text)
    # Human-readable reason for the category

    job: Mapped["ReplayJob"] = relationship("ReplayJob", back_populates="results")
    recording: Mapped["Recording"] = relationship("Recording", back_populates="replay_results")
