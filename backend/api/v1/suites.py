"""
Replay Suite management — group multiple test cases and run them in one shot.
"""
import asyncio
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.suite import ReplaySuite, SuiteRun
from models.test_case import TestCase
from models.application import Application
from schemas.suite import SuiteCreate, SuiteUpdate, SuiteOut, SuiteRunRequest, SuiteRunOut

router = APIRouter(prefix="/suites", tags=["suites"])

_background_tasks: set = set()

def _fire(coro):
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)


# ── CRUD ──────────────────────────────────────────────────────────────────────

@router.post("", response_model=SuiteOut, status_code=201)
async def create_suite(body: SuiteCreate, db: AsyncSession = Depends(get_db)):
    suite = ReplaySuite(id=str(uuid.uuid4()), **body.model_dump())
    db.add(suite)
    await db.commit()
    await db.refresh(suite)
    return suite


@router.get("", response_model=list[SuiteOut])
async def list_suites(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ReplaySuite).order_by(ReplaySuite.created_at.desc()))
    return result.scalars().all()


@router.get("/{suite_id}", response_model=SuiteOut)
async def get_suite(suite_id: str, db: AsyncSession = Depends(get_db)):
    suite = await db.get(ReplaySuite, suite_id)
    if not suite:
        raise HTTPException(404, "Suite not found")
    return suite


@router.put("/{suite_id}", response_model=SuiteOut)
async def update_suite(suite_id: str, body: SuiteUpdate, db: AsyncSession = Depends(get_db)):
    suite = await db.get(ReplaySuite, suite_id)
    if not suite:
        raise HTTPException(404, "Suite not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(suite, field, value)
    suite.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(suite)
    return suite


@router.delete("/{suite_id}", status_code=204)
async def delete_suite(suite_id: str, db: AsyncSession = Depends(get_db)):
    suite = await db.get(ReplaySuite, suite_id)
    if not suite:
        raise HTTPException(404, "Suite not found")
    await db.delete(suite)
    await db.commit()


# ── Suite Runs ────────────────────────────────────────────────────────────────

@router.post("/{suite_id}/runs", response_model=SuiteRunOut, status_code=201)
async def run_suite(
    suite_id: str,
    body: SuiteRunRequest,
    db: AsyncSession = Depends(get_db),
):
    suite = await db.get(ReplaySuite, suite_id)
    if not suite:
        raise HTTPException(404, "Suite not found")

    # Resolve effective target app: per-run override > suite default
    target_app_id = body.target_app_id or suite.default_target_app_id
    # Build effective case_app_map: suite-level map merged with run-level overrides
    effective_case_app_map: dict[str, str] = {}
    if suite.case_app_map:
        effective_case_app_map.update(suite.case_app_map)
    if body.case_app_map:
        effective_case_app_map.update(body.case_app_map)

    # Ensure every case has a resolvable target app
    if not target_app_id and suite.case_ids:
        missing = [cid for cid in suite.case_ids if cid not in effective_case_app_map]
        if missing:
            raise HTTPException(
                400,
                f"No target_app_id for case(s): {missing}. "
                "Provide target_app_id or case_app_map covering all cases."
            )

    # Validate global target app if provided
    if target_app_id:
        app = await db.get(Application, target_app_id)
        if not app:
            raise HTTPException(404, "Target application not found")

    if not suite.case_ids:
        raise HTTPException(400, "Suite has no test cases")

    # Validate all cases exist
    for case_id in suite.case_ids:
        tc = await db.get(TestCase, case_id)
        if not tc:
            raise HTTPException(400, f"Test case {case_id} not found")

    run = SuiteRun(
        id=str(uuid.uuid4()),
        suite_id=suite_id,
        target_app_id=target_app_id,
        status="RUNNING",
        total_cases=len(suite.case_ids),
        started_at=datetime.utcnow(),
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)

    _fire(_run_suite(run.id, suite_id, body, effective_case_app_map))
    return run


@router.get("/{suite_id}/runs", response_model=list[SuiteRunOut])
async def list_suite_runs(suite_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SuiteRun)
        .where(SuiteRun.suite_id == suite_id)
        .order_by(SuiteRun.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


@router.get("/{suite_id}/runs/{run_id}", response_model=SuiteRunOut)
async def get_suite_run(suite_id: str, run_id: str, db: AsyncSession = Depends(get_db)):
    run = await db.get(SuiteRun, run_id)
    if not run or run.suite_id != suite_id:
        raise HTTPException(404, "Suite run not found")
    return run


# ── Background worker ─────────────────────────────────────────────────────────

async def _run_suite(run_id: str, suite_id: str, req: SuiteRunRequest, case_app_map: dict[str, str] | None = None):
    from database import async_session_factory
    from api.v1.replays import _run_replay_job
    from models.replay import ReplayJob
    from models.test_case import TestCase, TestCaseRecording
    from sqlalchemy import select

    job_ids: list[str] = []
    try:
        async with async_session_factory() as db:
            run = await db.get(SuiteRun, run_id)
            suite = await db.get(ReplaySuite, suite_id)
            if not run or not suite:
                return

            # Merge suite defaults with run overrides
            concurrency = req.concurrency or suite.default_concurrency or 1
            ignore_fields = req.ignore_fields or suite.default_ignore_fields or []
            diff_rules = req.diff_rules or suite.default_diff_rules or []
            assertions = req.assertions or suite.default_assertions or []
            perf_threshold_ms = req.perf_threshold_ms or suite.default_perf_threshold_ms
            environment = req.environment or suite.default_environment
            override_host = req.override_host or suite.default_override_host
            delay_ms = suite.default_delay_ms or 0

            case_ids = list(suite.case_ids)

            # Create one replay job per test case (skip cases with no recordings)
            for case_id in case_ids:
                tc = await db.get(TestCase, case_id)
                if not tc:
                    continue
                has_recs = await db.execute(
                    select(TestCaseRecording).where(TestCaseRecording.case_id == case_id).limit(1)
                )
                if not has_recs.scalars().first():
                    continue

                job_id = str(uuid.uuid4())
                # Resolve per-case target app: case_app_map > global default
                effective_app_id = (
                    (case_app_map or {}).get(case_id)
                    or req.target_app_id
                    or suite.default_target_app_id
                )
                if not effective_app_id:
                    print(f"[suite] No target app for case {case_id}, skipping")
                    continue

                job = ReplayJob(
                    id=job_id,
                    case_id=case_id,
                    target_app_id=effective_app_id,
                    total_count=tc.recording_count,
                    concurrency=concurrency,
                    delay_ms=delay_ms,
                    ignore_fields=ignore_fields,
                    diff_rules=diff_rules,
                    assertions=assertions,
                    perf_threshold_ms=perf_threshold_ms,
                    override_host=override_host,
                    environment=environment or "suite",
                    created_by=f"suite_run:{run_id}",
                )
                db.add(job)
                job_ids.append(job_id)

            # Fix Bug 1: update total_cases to reflect actually runnable cases
            run.job_ids = job_ids
            run.total_cases = len(job_ids)
            await db.commit()

        # Run all jobs concurrently
        await asyncio.gather(*[_run_replay_job(jid) for jid in job_ids], return_exceptions=True)

        # Tally results
        async with async_session_factory() as db:
            run = await db.get(SuiteRun, run_id)
            if not run:
                return

            from models.replay import ReplayJob as RJ
            total_req = 0
            passed_req = 0
            passed_cases = 0
            failed_cases = 0

            for jid in job_ids:
                job = await db.get(RJ, jid)
                if not job:
                    continue
                sent = job.sent_count or 0
                success = job.success_count or 0
                total_req += sent
                passed_req += success
                if sent > 0 and success == sent:
                    passed_cases += 1
                else:
                    failed_cases += 1

            run.total_requests = total_req
            run.passed_requests = passed_req
            run.passed_cases = passed_cases
            run.failed_cases = failed_cases
            run.overall_pass_rate = passed_req / total_req if total_req else 0.0
            run.status = "DONE"
            run.finished_at = datetime.utcnow()
            await db.commit()

    except Exception as e:
        # Fix Bug 2: mark run as FAILED on unhandled exception
        print(f"[suite] _run_suite failed for run {run_id}: {e}")
        try:
            from database import async_session_factory as sf
            async with sf() as db:
                run = await db.get(SuiteRun, run_id)
                if run and run.status == "RUNNING":
                    run.status = "FAILED"
                    run.finished_at = datetime.utcnow()
                    await db.commit()
        except Exception:
            pass
