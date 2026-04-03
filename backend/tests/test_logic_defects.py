"""
测试核心业务逻辑的缺陷
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
import uuid
from datetime import datetime


class TestApplicationDeletion:
    """测试应用删除的级联逻辑 — 通过 API 端点测试"""

    def test_delete_application_cascade(self, tmp_path):
        """删除应用时，关联的 Session / Recording / TestCase 应被级联删除"""
        import database
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from database import get_db, Base
        from main import app
        from fastapi.testclient import TestClient

        db_file = str(tmp_path / "cascade_test.db")
        db_url = f"sqlite+aiosqlite:///{db_file}"
        test_engine = create_async_engine(db_url, echo=False)
        test_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

        old_engine = database.engine
        old_factory = database.async_session_factory
        database.engine = test_engine
        database.async_session_factory = test_factory

        async def _override_get_db():
            async with test_factory() as session:
                yield session

        app.dependency_overrides[get_db] = _override_get_db

        with TestClient(app, raise_server_exceptions=False) as client:
            # Create app
            r = client.post("/api/v1/applications", json={
                "name": "cascade-app",
                "ssh_host": "localhost",
                "ssh_user": "test",
            })
            assert r.status_code == 201
            app_id = r.json()["id"]

            # Create session
            r = client.post("/api/v1/sessions", json={
                "app_id": app_id,
                "name": "cascade-session",
            })
            assert r.status_code == 201
            session_id = r.json()["id"]

            # Delete application
            r = client.delete(f"/api/v1/applications/{app_id}")
            assert r.status_code == 204

            # Session should be gone
            r = client.get(f"/api/v1/sessions/{session_id}")
            assert r.status_code == 404

        app.dependency_overrides.clear()
        database.engine = old_engine
        database.async_session_factory = old_factory


class TestReplayJobLogic:
    """测试回放任务逻辑"""

    def test_replay_job_status_transitions(self):
        """测试回放任务状态转换"""
        from models.replay import ReplayJob
        
        job = ReplayJob(
            id=str(uuid.uuid4()),
            case_id=str(uuid.uuid4()),
            target_app_id=str(uuid.uuid4()),
            status="PENDING"
        )
        
        assert job.status == "PENDING"
        
        valid_statuses = ["RUNNING", "DONE", "FAILED", "CANCELLED"]
        
        for status in valid_statuses:
            job.status = status
            assert job.status == status

    def test_replay_result_default_values(self):
        """测试回放结果默认值"""
        from models.replay import ReplayResult
        
        result = ReplayResult(
            id=str(uuid.uuid4()),
            job_id=str(uuid.uuid4()),
            recording_id=str(uuid.uuid4())
        )
        
        assert result.status is None
        assert result.diff_score is None


class TestCompareLogic:
    """测试 A/B 对比逻辑"""

    def test_compare_result_calculation(self):
        """测试对比结果计算"""
        from models.compare import CompareRun, CompareResult
        
        run = CompareRun(
            id=str(uuid.uuid4()),
            name="test-compare",
            case_id=str(uuid.uuid4()),
            app_a_id=str(uuid.uuid4()),
            app_b_id=str(uuid.uuid4()),
            status="RUNNING"
        )
        
        assert run.status == "RUNNING"
        assert run.agreed_count == 0
        assert run.diverged_count == 0


class TestScheduleLogic:
    """测试定时任务逻辑"""

    def test_cron_expression_no_validation(self):
        """缺陷: 没有对 cron 表达式进行验证"""
        from models.schedule import ScheduledReplay
        
        # 无效的 cron 表达式也被接受
        invalid_schedule = ScheduledReplay(
            id=str(uuid.uuid4()),
            name="invalid",
            case_id=str(uuid.uuid4()),
            target_app_id=str(uuid.uuid4()),
            cron_expr="invalid-cron"  # 没有验证格式
        )
        
        # 代码接受了这个无效值
        assert invalid_schedule.cron_expr == "invalid-cron"


class TestDiffLogic:
    """测试 Diff 逻辑缺陷"""

    def test_ignore_fields_working(self):
        """测试忽略字段功能 — 支持 ignore_fields 关键字参数"""
        from utils.diff import compute_diff

        original = '{"timestamp": 1234567890, "data": {"id": 1, "name": "test"}}'
        replayed = '{"timestamp": 9876543210, "data": {"id": 1, "name": "test"}}'

        # ignore_fields is a user-facing keyword alias for auto-converted regex patterns
        diff_json, score = compute_diff(
            original,
            replayed,
            ignore_fields=["timestamp"]
        )

        assert score == 0.0, "timestamp should be ignored"

    def test_numeric_tolerance_rule(self):
        """测试数值容差规则"""
        from utils.diff import compute_diff
        
        original = '{"price": 100.0}'
        replayed = '{"price": 100.05}'
        
        diff_json, score = compute_diff(
            original,
            replayed,
            diff_rules=[{"type": "numeric_tolerance", "path": "price", "tolerance": 0.1}]
        )
        
        assert score == 0.0


class TestSSHExecutor:
    """测试 SSH 执行器"""

    def test_sftp_has_finally_block(self):
        """验证 SFTP 连接有正确关闭逻辑"""
        with open("integration/ssh_executor.py", "r") as f:
            content = f.read()
        
        assert "finally:" in content
        assert "sftp.close()" in content
        assert "client.close()" in content


class TestSchedulerTimezone:
    """测试调度器时区"""

    def test_scheduler_timezone_config(self):
        """测试调度器时区设置"""
        from core.scheduler import scheduler
        
        assert "Shanghai" in str(scheduler.timezone)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
