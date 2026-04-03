import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class RepeaterConfig(Base):
    __tablename__ = "repeater_config"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    app_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)
    config_json: Mapped[str] = mapped_column(Text, nullable=False)
    plugins: Mapped[list | None] = mapped_column(JSON)  # ["http", "mybatis", "dubbo-provider"]
    sampling_rate: Mapped[float] = mapped_column(Float, default=1.0)
    include_paths: Mapped[list | None] = mapped_column(JSON)
    exclude_paths: Mapped[list | None] = mapped_column(JSON)
    # P1-3: 录制自动停止
    max_duration_seconds: Mapped[int | None] = mapped_column(Integer)  # 最大录制时长（秒），0 或空表示不限制
    max_record_count: Mapped[int | None] = mapped_column(Integer)  # 最大录制条数，0 或空表示不限制
    pushed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    application: Mapped["Application"] = relationship("Application", back_populates="repeater_config")


class RecordingSession(Base):
    __tablename__ = "recording_session"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    app_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)
    name: Mapped[str | None] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    # ACTIVE / STOPPED / COLLECTING / DONE / ERROR
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime)
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    config_snapshot: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str | None] = mapped_column(String(128))
    error_message: Mapped[str | None] = mapped_column(Text)

    application: Mapped["Application"] = relationship("Application", back_populates="sessions")
    recordings: Mapped[list["Recording"]] = relationship(
        "Recording", back_populates="session", cascade="all, delete-orphan"
    )


class Recording(Base):
    __tablename__ = "recording"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("recording_session.id"), nullable=False
    )
    app_id: Mapped[str] = mapped_column(String(36), ForeignKey("application.id"), nullable=False)

    trace_id: Mapped[str | None] = mapped_column(String(64), index=True)
    entry_type: Mapped[str | None] = mapped_column(String(32))  # HTTP / DUBBO / JAVA / MYBATIS
    entry_app: Mapped[str | None] = mapped_column(String(128))

    host: Mapped[str | None] = mapped_column(String(256))
    path: Mapped[str | None] = mapped_column(String(512))  # HTTP URI or method signature
    request_body: Mapped[str | None] = mapped_column(Text)
    response_body: Mapped[str | None] = mapped_column(Text)
    sub_invocations: Mapped[list | None] = mapped_column(JSON)  # mock sub-calls (DB, RPC)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    timestamp: Mapped[datetime | None] = mapped_column(DateTime)

    tags: Mapped[list | None] = mapped_column(JSON)  # e.g. ["smoke", "P0"]
    status: Mapped[str] = mapped_column(String(32), default="RAW")
    # RAW / PARSED / ADDED_TO_CASE
    raw_file_path: Mapped[str | None] = mapped_column(String(512))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["RecordingSession"] = relationship("RecordingSession", back_populates="recordings")
    case_links: Mapped[list["TestCaseRecording"]] = relationship(
        "TestCaseRecording", back_populates="recording", cascade="all, delete-orphan"
    )
    replay_results: Mapped[list["ReplayResult"]] = relationship(
        "ReplayResult", back_populates="recording", cascade="all, delete-orphan"
    )
