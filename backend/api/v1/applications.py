import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from database import get_db
from models.application import Application
from schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationOut, SSHTestResult
from integration import ssh_executor
from integration import repeater_client
import uuid
from datetime import datetime

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationOut, status_code=201)
async def create_application(body: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    app = Application(id=str(uuid.uuid4()), **body.model_dump())
    db.add(app)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, f"Application name '{body.name}' already exists")
    await db.refresh(app)
    return app


@router.get("", response_model=list[ApplicationOut])
async def list_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).order_by(Application.created_at.desc()))
    return result.scalars().all()


@router.get("/{app_id}", response_model=ApplicationOut)
async def get_application(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    return app


@router.put("/{app_id}", response_model=ApplicationOut)
async def update_application(
    app_id: str, body: ApplicationUpdate, db: AsyncSession = Depends(get_db)
):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(app, field, value)
    app.updated_at = datetime.utcnow()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, f"Application name already exists")
    await db.refresh(app)
    return app


@router.delete("/{app_id}", status_code=204)
async def delete_application(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")

    from models.replay import ReplayJob, ReplayResult
    from models.schedule import ScheduledReplay
    from models.recording import RecordingSession, Recording, RepeaterConfig
    from models.test_case import TestCase, TestCaseRecording
    from models.compare import CompareRun, CompareResult as CompareResultModel

    # 0. 删除应用的 Repeater 配置
    await db.execute(delete(RepeaterConfig).where(RepeaterConfig.app_id == app_id))

    # 0b. 删除以此应用为 A 或 B 的双环境对比记录
    compare_run_ids_result = await db.execute(
        select(CompareRun.id).where(
            (CompareRun.app_a_id == app_id) | (CompareRun.app_b_id == app_id)
        )
    )
    compare_run_ids = compare_run_ids_result.scalars().all()
    if compare_run_ids:
        await db.execute(delete(CompareResultModel).where(CompareResultModel.run_id.in_(compare_run_ids)))
        await db.execute(delete(CompareRun).where(CompareRun.id.in_(compare_run_ids)))

    # 1. 删除定时回放任务
    await db.execute(delete(ScheduledReplay).where(ScheduledReplay.target_app_id == app_id))

    # 2. 删除以此应用为目标的回放任务及其结果
    job_ids_result = await db.execute(
        select(ReplayJob.id).where(ReplayJob.target_app_id == app_id)
    )
    job_ids = job_ids_result.scalars().all()
    if job_ids:
        await db.execute(delete(ReplayResult).where(ReplayResult.job_id.in_(job_ids)))
        await db.execute(delete(ReplayJob).where(ReplayJob.target_app_id == app_id))

    # 3. 删除此应用的录制数据（需手动级联，async 模式 ORM 级联不可靠）
    session_ids_result = await db.execute(
        select(RecordingSession.id).where(RecordingSession.app_id == app_id)
    )
    session_ids = session_ids_result.scalars().all()
    if session_ids:
        rec_ids_result = await db.execute(
            select(Recording.id).where(Recording.session_id.in_(session_ids))
        )
        rec_ids = rec_ids_result.scalars().all()
        if rec_ids:
            await db.execute(delete(TestCaseRecording).where(TestCaseRecording.recording_id.in_(rec_ids)))
            await db.execute(delete(ReplayResult).where(ReplayResult.recording_id.in_(rec_ids)))
            await db.execute(delete(Recording).where(Recording.id.in_(rec_ids)))
        await db.execute(delete(RecordingSession).where(RecordingSession.id.in_(session_ids)))

    # 4. 删除此应用的测试用例（及关联的 TestCaseRecording 条目）
    case_ids_result = await db.execute(
        select(TestCase.id).where(TestCase.app_id == app_id)
    )
    case_ids = case_ids_result.scalars().all()
    if case_ids:
        await db.execute(delete(TestCaseRecording).where(TestCaseRecording.case_id.in_(case_ids)))
        await db.execute(delete(TestCase).where(TestCase.app_id == app_id))

    await db.delete(app)
    await db.commit()


# ── Agent operations ──────────────────────────────────────────────────────────

@router.post("/{app_id}/agent/ssh-test", response_model=SSHTestResult)
async def test_ssh(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    result = await asyncio.to_thread(ssh_executor.test_connection, app)
    return SSHTestResult(**result)


@router.post("/{app_id}/agent/discover-pid", response_model=dict)
async def discover_pid(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    pid = await asyncio.to_thread(ssh_executor.discover_pid, app)
    if pid:
        app.java_pid = pid
        app.updated_at = datetime.utcnow()
        await db.commit()
    return {"pid": pid}


@router.post("/{app_id}/agent/attach", response_model=dict)
async def attach_agent(app_id: str, db: AsyncSession = Depends(get_db)):
    """
    Attach JVM-Sandbox Repeater agent to the target JVM.
    Steps: discover PID → push sandbox + config → run attach command.
    """
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")

    # 1. Discover PID
    pid = await asyncio.to_thread(ssh_executor.discover_pid, app)
    if not pid:
        raise HTTPException(400, "Could not discover JVM PID. Check java_jar_name setting.")
    app.java_pid = pid

    # 2. Run sandbox attach script on remote host
    attach_cmd = (
        f"source /etc/profile; "
        f"cd {app.sandbox_home}/bin && "
        f"bash sandbox.sh -p {pid} -P {app.sandbox_port}"
    )
    exit_code, stdout, stderr = await asyncio.to_thread(
        ssh_executor.run_command, app, attach_cmd, 30
    )

    if exit_code != 0:
        app.agent_status = "ERROR"
        await db.commit()
        raise HTTPException(500, f"Attach failed: {stderr}")

    # 3. Mark as ATTACHED (recording is handled by the built-in Spring Boot filter,
    #    not the JVM-Sandbox management port, so no HTTP liveness check needed)
    app.agent_status = "ATTACHED"
    app.last_heartbeat = datetime.utcnow()
    app.updated_at = datetime.utcnow()
    await db.commit()

    return {"agent_status": "ATTACHED", "pid": pid, "stdout": stdout}


@router.post("/{app_id}/agent/detach", response_model=dict)
async def detach_agent(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")

    if not app.java_pid:
        raise HTTPException(400, "No known PID; agent may not be attached")

    detach_cmd = (
        f"source /etc/profile; "
        f"cd {app.sandbox_home}/bin && "
        f"bash sandbox.sh -p {app.java_pid} -P {app.sandbox_port} -S"
    )
    exit_code, stdout, stderr = await asyncio.to_thread(
        ssh_executor.run_command, app, detach_cmd, 15
    )

    if exit_code != 0:
        app.agent_status = "ERROR"
        app.updated_at = datetime.utcnow()
        await db.commit()
        raise HTTPException(500, f"Detach failed: {stderr}")

    app.agent_status = "DETACHED"
    app.updated_at = datetime.utcnow()
    await db.commit()
    return {"agent_status": "DETACHED", "stdout": stdout}


@router.get("/{app_id}/agent/status", response_model=dict)
async def agent_status(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    result = await repeater_client.check_agent_status(app)
    if result.get("alive"):
        app.agent_status = "ATTACHED"
        app.last_heartbeat = datetime.utcnow()
        await db.commit()
    return {"alive": result.get("alive"), "agent_status": app.agent_status}
