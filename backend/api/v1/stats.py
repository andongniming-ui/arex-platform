"""
Statistics & trend analytics endpoints.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models.replay import ReplayJob

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/trend")
async def get_trend(
    app_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    """
    Return daily pass-rate trend for the last N days.
    Each item: {date, total, pass, fail, error, pass_rate}
    """
    since = datetime.utcnow() - timedelta(days=days)
    q = select(ReplayJob).where(
        ReplayJob.finished_at >= since,
        ReplayJob.status.in_(["DONE", "FAILED"]),
    )
    if app_id:
        q = q.where(ReplayJob.target_app_id == app_id)
    result = await db.execute(q)
    jobs = result.scalars().all()

    # Group by local date (finished_at stored as UTC, shift to +8 for display)
    by_date: dict[str, dict] = {}
    for job in jobs:
        if not job.finished_at:
            continue
        # Add 8 hours to convert UTC → CST for grouping
        local_dt = job.finished_at + timedelta(hours=8)
        date_key = local_dt.strftime("%Y-%m-%d")
        if date_key not in by_date:
            by_date[date_key] = {"total": 0, "pass": 0, "fail": 0, "error": 0}
        sent = job.sent_count or 0
        success = job.success_count or 0
        fail = job.fail_count or 0
        error = max(sent - success - fail, 0)
        by_date[date_key]["total"] += sent
        by_date[date_key]["pass"] += success
        by_date[date_key]["fail"] += fail
        by_date[date_key]["error"] += error

    # Build full date series (fill gaps with zeros)
    series = []
    for i in range(days):
        local_now = datetime.utcnow() + timedelta(hours=8)
        date = (local_now - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        d = by_date.get(date, {"total": 0, "pass": 0, "fail": 0, "error": 0})
        pass_rate = round(d["pass"] / d["total"] * 100, 1) if d["total"] > 0 else 0.0
        series.append({
            "date": date,
            "total": d["total"],
            "pass": d["pass"],
            "fail": d["fail"],
            "error": d["error"],
            "pass_rate": pass_rate,
        })

    return series


@router.get("/daily-jobs")
async def get_daily_jobs(
    date: str,
    app_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Return replay jobs whose finished_at falls on `date` (YYYY-MM-DD, CST/UTC+8).
    """
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(400, "date must be YYYY-MM-DD")
    # CST date 00:00 → UTC: subtract 8h
    start_utc = d - timedelta(hours=8)
    end_utc = start_utc + timedelta(days=1)
    q = (
        select(ReplayJob)
        .where(
            ReplayJob.finished_at >= start_utc,
            ReplayJob.finished_at < end_utc,
            ReplayJob.status.in_(["DONE", "FAILED"]),
        )
        .order_by(ReplayJob.finished_at.desc())
    )
    if app_id:
        q = q.where(ReplayJob.target_app_id == app_id)
    result = await db.execute(q)
    jobs = result.scalars().all()
    return [
        {
            "id": j.id,
            "case_id": j.case_id,
            "target_app_id": j.target_app_id,
            "status": j.status,
            "environment": j.environment,
            "total_count": j.total_count,
            "sent_count": j.sent_count,
            "success_count": j.success_count,
            "fail_count": j.fail_count,
            "finished_at": j.finished_at.isoformat() if j.finished_at else None,
        }
        for j in jobs
    ]


@router.get("/summary")
async def get_summary(
    app_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Overall totals: total replays, avg pass rate, jobs count."""
    q = (
        select(
            func.count(ReplayJob.id).label("job_count"),
            func.coalesce(func.sum(ReplayJob.sent_count), 0).label("total_sent"),
            func.coalesce(func.sum(ReplayJob.success_count), 0).label("total_pass"),
            func.coalesce(func.sum(ReplayJob.fail_count), 0).label("total_fail"),
        )
        .where(ReplayJob.status == "DONE")
    )
    if app_id:
        q = q.where(ReplayJob.target_app_id == app_id)
    row = (await db.execute(q)).one()

    total_sent = row.total_sent or 0
    total_pass = row.total_pass or 0
    total_fail = row.total_fail or 0
    total_error = max(total_sent - total_pass - total_fail, 0)
    avg_pass_rate = round(total_pass / total_sent * 100, 1) if total_sent else 0.0

    return {
        "job_count": row.job_count,
        "total_sent": total_sent,
        "total_pass": total_pass,
        "total_fail": total_fail,
        "total_error": total_error,
        "avg_pass_rate": avg_pass_rate,
    }
