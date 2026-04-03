import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class TestCase(Base):
    __tablename__ = "test_case"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    app_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("application.id"))
    tags: Mapped[list | None] = mapped_column(JSON)  # ["smoke", "regression"]
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    recording_count: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    recordings: Mapped[list["TestCaseRecording"]] = relationship(
        "TestCaseRecording",
        back_populates="test_case",
        cascade="all, delete-orphan",
        order_by="TestCaseRecording.sort_order",
    )
    replay_jobs: Mapped[list["ReplayJob"]] = relationship(
        "ReplayJob", back_populates="test_case"
    )


class TestCaseRecording(Base):
    __tablename__ = "test_case_recording"
    __table_args__ = (UniqueConstraint("case_id", "recording_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_case.id"), nullable=False)
    recording_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("recording.id"), nullable=False
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test_case: Mapped["TestCase"] = relationship("TestCase", back_populates="recordings")
    recording: Mapped["Recording"] = relationship("Recording", back_populates="case_links")
