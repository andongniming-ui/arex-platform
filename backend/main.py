import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db, async_session_factory
from api.v1 import applications, sessions, test_cases, replays, ci
from api.v1 import schedule as schedule_api
from api.v1 import stats as stats_api
from api.v1 import suites as suites_api
from api.v1 import compare as compare_api
from api.v1.replays import _run_replay_job
from api.v1.schedule import load_all_schedules
from core.scheduler import scheduler


async def _recover_on_startup():
    """
    On restart, recover interrupted tasks:
    - PENDING replay jobs - re-launch background execution
    - RUNNING replay jobs - mark FAILED (state is unknown after crash)
    - COLLECTING sessions - mark ERROR (collection task was lost)
    """
    from sqlalchemy import select, update
    from models.replay import ReplayJob
    from models.recording import RecordingSession

    async with async_session_factory() as db:
        # 1. Mark RUNNING jobs as FAILED
        await db.execute(
            update(ReplayJob)
            .where(ReplayJob.status == "RUNNING")
            .values(status="FAILED")
        )

        # 2. Re-queue PENDING jobs
        result = await db.execute(
            select(ReplayJob.id).where(ReplayJob.status == "PENDING")
        )
        pending_ids = result.scalars().all()

        # 3. Mark COLLECTING sessions as ERROR
        await db.execute(
            update(RecordingSession)
            .where(RecordingSession.status == "COLLECTING")
            .values(status="ERROR")
        )

        await db.commit()

    for job_id in pending_ids:
        asyncio.create_task(_run_replay_job(job_id))

    if pending_ids:
        print(f"[startup] Re-queued {len(pending_ids)} PENDING replay job(s): {pending_ids}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await _recover_on_startup()
    await load_all_schedules()
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="AREX Platform",
    description="Java traffic record-replay management platform backed by AREX agent",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(applications.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(test_cases.router, prefix="/api/v1")
app.include_router(replays.router, prefix="/api/v1")
app.include_router(ci.router, prefix="/api/v1")
app.include_router(schedule_api.router, prefix="/api/v1")
app.include_router(stats_api.router, prefix="/api/v1")
app.include_router(suites_api.router, prefix="/api/v1")
app.include_router(compare_api.router, prefix="/api/v1")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
