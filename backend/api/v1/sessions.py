import asyncio
import uuid
import json as _json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from database import get_db
from models.application import Application
from models.recording import RecordingSession, Recording, RepeaterConfig
from models.test_case import TestCaseRecording
from schemas.recording import SessionCreate, SessionOut, RecordingOut, RepeaterConfigCreate, RepeaterConfigOut
from integration import ssh_executor, config_manager, data_parser
from utils.desensitize import desensitize_body

router = APIRouter(tags=["sessions & recordings"])


async def _get_app_with_config(app_id: str, db: AsyncSession) -> Application:
    """Fetch application with repeater_config eagerly loaded."""
    result = await db.execute(
        select(Application)
        .where(Application.id == app_id)
        .options(selectinload(Application.repeater_config))
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application not found")
    return app


# ── Config ────────────────────────────────────────────────────────────────────

@router.get("/configs/{app_id}", response_model=RepeaterConfigOut)
async def get_config(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await _get_app_with_config(app_id, db)
    if not app.repeater_config:
        raise HTTPException(404, "No config found; POST to create one")
    return app.repeater_config


@router.put("/configs/{app_id}", response_model=RepeaterConfigOut)
async def upsert_config(
    app_id: str, body: RepeaterConfigCreate, db: AsyncSession = Depends(get_db)
):
    import json as _json
    app = await _get_app_with_config(app_id, db)

    # Validate config_json is non-empty valid JSON with required fields
    try:
        parsed = _json.loads(body.config_json)
    except Exception:
        raise HTTPException(400, "config_json is not valid JSON")
    if not isinstance(parsed, dict) or not parsed.get("pluginIdentities"):
        raise HTTPException(400, "config_json must include pluginIdentities")

    if app.repeater_config:
        cfg = app.repeater_config
        for field, value in body.model_dump().items():
            setattr(cfg, field, value)
        cfg.updated_at = datetime.utcnow()
    else:
        cfg = RepeaterConfig(id=str(uuid.uuid4()), app_id=app_id, **body.model_dump())
        db.add(cfg)
    await db.commit()
    await db.refresh(cfg)
    return cfg


@router.post("/configs/{app_id}/push", response_model=dict)
async def push_config(app_id: str, db: AsyncSession = Depends(get_db)):
    app = await _get_app_with_config(app_id, db)
    if not app.repeater_config:
        raise HTTPException(400, "No config to push; create config first")
    await config_manager.push_config(app, app.repeater_config)
    app.repeater_config.pushed_at = datetime.utcnow()
    await db.commit()
    return {"pushed": True, "pushed_at": app.repeater_config.pushed_at.isoformat()}


@router.get("/configs/{app_id}/default", response_model=dict)
async def get_default_config(app_id: str):
    import json
    return {"config": json.loads(config_manager.get_default_config_json())}


# ── Sessions ──────────────────────────────────────────────────────────────────

@router.post("/sessions", response_model=SessionOut, status_code=201)
async def create_session(body: SessionCreate, db: AsyncSession = Depends(get_db)):
    app = await _get_app_with_config(body.app_id, db)

    # Clear remote recording directory so old files don't contaminate this session
    try:
        deleted = await asyncio.to_thread(
            ssh_executor.clear_remote_dir, app, app.repeater_data_dir
        )
        if deleted:
            print(f"[session] Cleared {deleted} old file(s) from {app.repeater_data_dir}")
    except Exception as e:
        print(f"[session] Warning: could not clear remote recording dir: {e}")

    # Snapshot current config
    config_snapshot = app.repeater_config.config_json if app.repeater_config else None

    session = RecordingSession(
        id=str(uuid.uuid4()),
        config_snapshot=config_snapshot,
        **body.model_dump(),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.get("/sessions", response_model=dict)
async def list_sessions(
    app_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    base = select(RecordingSession)
    if app_id:
        base = base.where(RecordingSession.app_id == app_id)
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar() or 0
    items = (await db.execute(base.order_by(RecordingSession.started_at.desc()).offset(offset).limit(limit))).scalars().all()
    return {"items": [SessionOut.model_validate(i) for i in items], "total": total}


@router.get("/sessions/{session_id}", response_model=SessionOut)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    s = await db.get(RecordingSession, session_id)
    if not s:
        raise HTTPException(404, "Session not found")
    return s


@router.delete("/sessions/batch", status_code=204)
async def batch_delete_sessions(body: dict, db: AsyncSession = Depends(get_db)):
    """Delete multiple sessions by ID. Body: {"ids": [...]}"""
    ids = body.get("ids") or []
    if not ids:
        return
    from models.replay import ReplayResult
    result = await db.execute(
        select(Recording.id).where(Recording.session_id.in_(ids))
    )
    recording_ids = result.scalars().all()
    if recording_ids:
        await db.execute(
            delete(TestCaseRecording).where(TestCaseRecording.recording_id.in_(recording_ids))
        )
        await db.execute(
            delete(ReplayResult).where(ReplayResult.recording_id.in_(recording_ids))
        )
        await db.execute(
            delete(Recording).where(Recording.session_id.in_(ids))
        )
    await db.execute(
        delete(RecordingSession).where(RecordingSession.id.in_(ids))
    )
    await db.commit()


@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    s = await db.get(RecordingSession, session_id)
    if not s:
        raise HTTPException(404, "Session not found")
    # Get recording IDs under this session
    result = await db.execute(
        select(Recording.id).where(Recording.session_id == session_id)
    )
    recording_ids = result.scalars().all()
    if recording_ids:
        # Delete test_case_recording links
        await db.execute(
            delete(TestCaseRecording).where(TestCaseRecording.recording_id.in_(recording_ids))
        )
        # Delete replay_results
        from models.replay import ReplayResult
        await db.execute(
            delete(ReplayResult).where(ReplayResult.recording_id.in_(recording_ids))
        )
        # Delete recordings
        await db.execute(
            delete(Recording).where(Recording.session_id == session_id)
        )
    await db.delete(s)
    await db.commit()


@router.put("/sessions/{session_id}/stop", response_model=dict)
async def stop_session(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    # Atomic conditional update: only transition ACTIVE → COLLECTING once
    result = await db.execute(
        update(RecordingSession)
        .where(RecordingSession.id == session_id, RecordingSession.status == "ACTIVE")
        .values(status="COLLECTING", stopped_at=datetime.utcnow())
    )
    await db.commit()
    if result.rowcount == 0:
        s = await db.get(RecordingSession, session_id)
        if not s:
            raise HTTPException(404, "Session not found")
        raise HTTPException(400, f"Session is {s.status}, not ACTIVE")

    background_tasks.add_task(_collect_recordings, session_id)
    return {"session_id": session_id, "status": "COLLECTING"}


async def _collect_recordings(session_id: str):
    """Background task: SFTP-pull recording files and store in DB."""
    import random
    from database import async_session_factory

    async with async_session_factory() as db:
        s = await db.get(RecordingSession, session_id)
        if not s:
            return
        app = await db.get(Application, s.app_id)
        if not app:
            return
        count = 0
        try:
            # Only collect files created after the session started (avoids mixing other apps' data)
            from datetime import timezone as _tz
            since_ts = s.started_at.replace(tzinfo=_tz.utc).timestamp()
            files = await asyncio.wait_for(
                asyncio.to_thread(
                    ssh_executor.list_remote_files, app, app.repeater_data_dir, since_ts
                ),
                timeout=120.0,
            )
            expected_port_suffix = f":{app.repeater_port}" if app.repeater_port else None
            session_start = s.started_at
            session_stop = s.stopped_at
            sample_rate = getattr(app, "sample_rate", 1.0) or 1.0
            desensitize_rules = getattr(app, "desensitize_rules", None) or []
            # Collect all candidate recordings first, then deduplicate before inserting.
            # When JVM-Sandbox agent and RecordingFilter both run, they both write a file
            # per request — one with an empty body (agent) and one with the real body (filter).
            # Deduplication keeps only the best recording per (path, 5-second bucket).
            all_candidates: list[tuple[str, dict]] = []  # (fname, rec_data)
            processed_fnames: set[str] = set()

            for fname in files:
                remote_path = f"{app.repeater_data_dir}/{fname}"
                content = await asyncio.wait_for(
                    asyncio.to_thread(
                        ssh_executor.pull_file_content, app, remote_path
                    ),
                    timeout=60.0,
                )
                parsed = data_parser.parse_recording_file(content, session_id, s.app_id)
                file_accepted = False
                for rec_data in parsed:
                    # Filter 1: host port must match this app
                    if expected_port_suffix:
                        rec_host = rec_data.get("host") or ""
                        if rec_host and rec_host != "unknown" and expected_port_suffix not in rec_host:
                            continue
                    # Filter 2: internal timestamp must fall within session window
                    rec_ts = rec_data.get("timestamp")
                    if rec_ts and session_start:
                        if rec_ts < session_start:
                            continue
                        if session_stop and rec_ts > session_stop:
                            continue
                    # Filter 3: sampling rate
                    if sample_rate < 1.0 and random.random() > sample_rate:
                        continue
                    # Apply desensitization to request and response bodies
                    if desensitize_rules:
                        if rec_data.get("request_body"):
                            rec_data["request_body"] = desensitize_body(
                                rec_data["request_body"], desensitize_rules
                            )
                        if rec_data.get("response_body"):
                            rec_data["response_body"] = desensitize_body(
                                rec_data["response_body"], desensitize_rules
                            )
                    all_candidates.append((fname, rec_data))
                    file_accepted = True
                if file_accepted:
                    processed_fnames.add(fname)

            # Deduplicate: when JVM-Sandbox agent and RecordingFilter both run, both write
            # a file per request. The sandbox recording has an empty body; the filter
            # recording has the real body. They arrive within ~2 seconds of each other.
            # For each empty-body recording that has a nearby with-body recording (≤2s),
            # discard the empty-body one.
            def _has_body(rd: dict) -> bool:
                return '"body"' in (rd.get("request_body") or "")

            discarded: set[int] = set()
            without_body_idxs = [i for i, (_, rd) in enumerate(all_candidates) if not _has_body(rd)]
            with_body_idxs    = [i for i, (_, rd) in enumerate(all_candidates) if _has_body(rd)]

            for wb_i in without_body_idxs:
                wb_ts = all_candidates[wb_i][1].get("timestamp")
                if not wb_ts:
                    continue
                for b_i in with_body_idxs:
                    b_ts = all_candidates[b_i][1].get("timestamp")
                    if b_ts and abs((b_ts - wb_ts).total_seconds()) <= 2.0:
                        discarded.add(wb_i)
                        break

            for idx, (_, rec_data) in enumerate(all_candidates):
                if idx in discarded:
                    continue
                rec = Recording(id=str(uuid.uuid4()), **rec_data)
                db.add(rec)
                count += 1

            # Delete all processed remote files (including discarded duplicates)
            for fname in processed_fnames:
                remote_path = f"{app.repeater_data_dir}/{fname}"
                try:
                    await asyncio.to_thread(
                        ssh_executor.delete_remote_file, app, remote_path
                    )
                except Exception:
                    pass
            s.record_count = count
            s.status = "DONE"
        except Exception as e:
            import traceback
            print(f"[ERROR] collect_recordings failed: {e}")
            traceback.print_exc()
            s.record_count = count
            s.status = "ERROR"
            s.error_message = str(e)
        await db.commit()


# ── Recordings ────────────────────────────────────────────────────────────────

@router.get("/recordings", response_model=dict)
async def list_recordings(
    session_id: str | None = None,
    app_id: str | None = None,
    entry_type: str | None = None,
    path_contains: str | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    base = select(Recording)
    if session_id:
        base = base.where(Recording.session_id == session_id)
    if app_id:
        base = base.where(Recording.app_id == app_id)
    if entry_type:
        base = base.where(Recording.entry_type == entry_type.upper())
    if path_contains:
        base = base.where(Recording.path.ilike(f"%{path_contains}%"))
    if created_after:
        from datetime import datetime as _dt
        base = base.where(Recording.created_at >= _dt.fromisoformat(created_after.replace("Z", "+00:00")))
    if created_before:
        from datetime import datetime as _dt
        base = base.where(Recording.created_at <= _dt.fromisoformat(created_before.replace("Z", "+00:00")))
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar() or 0
    items = (await db.execute(base.order_by(Recording.created_at.desc()).offset(offset).limit(limit))).scalars().all()
    return {"items": [RecordingOut.model_validate(i) for i in items], "total": total}


@router.get("/recordings/{recording_id}", response_model=RecordingOut)
async def get_recording(recording_id: str, db: AsyncSession = Depends(get_db)):
    rec = await db.get(Recording, recording_id)
    if not rec:
        raise HTTPException(404, "Recording not found")
    return rec


@router.post("/recordings/import-har", response_model=dict)
async def import_har(
    file: UploadFile = File(...),
    app_id: str = Form(...),
    session_name: str = Form(default="HAR 导入"),
    db: AsyncSession = Depends(get_db),
):
    """
    Import recordings from a Chrome DevTools HAR file.
    Creates a new RecordingSession + one Recording per HAR entry.
    """
    from urllib.parse import urlparse, urlencode

    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")

    raw = await file.read()
    try:
        har = _json.loads(raw)
    except Exception:
        raise HTTPException(400, "Invalid JSON / not a valid HAR file")

    entries = har.get("log", {}).get("entries", [])
    if not entries:
        raise HTTPException(400, "HAR file contains no entries")

    # Create a completed session
    session = RecordingSession(
        id=str(uuid.uuid4()),
        app_id=app_id,
        name=session_name,
        status="DONE",
        started_at=datetime.utcnow(),
        stopped_at=datetime.utcnow(),
    )
    db.add(session)

    count = 0
    for entry in entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})

        method = (req.get("method") or "GET").upper()
        url = req.get("url") or ""
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path

        # Append query params from queryString array if not already in URL
        qs_pairs = req.get("queryString") or []
        if qs_pairs and not parsed.query:
            path += "?" + urlencode([(q["name"], q["value"]) for q in qs_pairs])
        elif parsed.query:
            path += "?" + parsed.query

        # Request body
        post_data = req.get("postData") or {}
        body_text = post_data.get("text") or ""
        content_type = post_data.get("mimeType") or ""

        request_body_obj = {
            "method": method,
            "uri": url,
            "body": body_text if body_text else None,
            "contentType": content_type if content_type else None,
        }

        # Response body
        resp_content = resp.get("content") or {}
        resp_text = resp_content.get("text") or ""

        # Timestamp
        started_str = entry.get("startedDateTime") or ""
        timestamp = None
        if started_str:
            try:
                timestamp = datetime.fromisoformat(started_str.replace("Z", "+00:00"))
            except Exception:
                pass

        duration_ms = int(entry.get("time") or 0)

        rec = Recording(
            id=str(uuid.uuid4()),
            session_id=session.id,
            app_id=app_id,
            entry_type="HTTP",
            host=host,
            path=path,
            request_body=_json.dumps(request_body_obj, ensure_ascii=False),
            response_body=resp_text or None,
            duration_ms=duration_ms,
            timestamp=timestamp,
            status="PARSED",
        )
        db.add(rec)
        count += 1

    session.record_count = count
    await db.commit()
    return {"session_id": session.id, "imported": count, "session_name": session_name}


@router.patch("/recordings/{recording_id}/request", response_model=RecordingOut)
async def update_request_body(
    recording_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    """Edit the request body of a recording (for parameter mutation testing).
    Body: {"request_body": "{...json string...}"}
    """
    rec = await db.get(Recording, recording_id)
    if not rec:
        raise HTTPException(404, "Recording not found")
    new_rb = body.get("request_body")
    if new_rb is None:
        raise HTTPException(400, "request_body field is required")
    # Validate it's parseable JSON
    try:
        _json.loads(new_rb)
    except Exception:
        raise HTTPException(400, "request_body must be a valid JSON string")
    rec.request_body = new_rb
    await db.commit()
    await db.refresh(rec)
    return rec


@router.patch("/recordings/{recording_id}/tags", response_model=RecordingOut)
async def update_tags(
    recording_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    """Update the tags list of a recording. Body: {"tags": ["smoke", "P0"]}"""
    rec = await db.get(Recording, recording_id)
    if not rec:
        raise HTTPException(404, "Recording not found")
    rec.tags = body.get("tags") or []
    await db.commit()
    await db.refresh(rec)
    return rec


@router.delete("/recordings/batch", status_code=204)
async def batch_delete_recordings(body: dict, db: AsyncSession = Depends(get_db)):
    """Delete multiple recordings by ID. Body: {"ids": [...]}"""
    ids = body.get("ids") or []
    if not ids:
        return
    from models.replay import ReplayResult
    await db.execute(
        delete(TestCaseRecording).where(TestCaseRecording.recording_id.in_(ids))
    )
    await db.execute(
        delete(ReplayResult).where(ReplayResult.recording_id.in_(ids))
    )
    await db.execute(
        delete(Recording).where(Recording.id.in_(ids))
    )
    await db.commit()


@router.post("/recordings/{recording_id}/recapture", response_model=RecordingOut)
async def recapture_response(recording_id: str, db: AsyncSession = Depends(get_db)):
    """Re-send the recorded request to the app and update response_body as baseline."""
    import json as _json
    import httpx
    rec = await db.get(Recording, recording_id)
    if not rec:
        raise HTTPException(404, "Recording not found")
    app = await db.get(Application, rec.app_id)
    if not app:
        raise HTTPException(404, "Application not found")

    req_info: dict = {}
    if rec.request_body:
        try:
            req_info = _json.loads(rec.request_body)
        except Exception:
            pass

    method = (req_info.get("method") or "GET").upper()
    uri = req_info.get("uri") or rec.path or "/"
    from urllib.parse import urlparse
    if uri.startswith("http"):
        parsed = urlparse(uri)
        path = parsed.path + ("?" + parsed.query if parsed.query else "")
    else:
        path = uri

    send_body = req_info.get("body") if method not in ("GET", "DELETE", "HEAD") else None
    headers = {}
    ct = req_info.get("contentType")
    if ct and send_body:
        headers["Content-Type"] = ct

    try:
        url = f"http://{app.ssh_host}:{app.repeater_port}{path}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.request(method=method, url=url, headers=headers,
                                     content=send_body.encode() if send_body else None)
        rec.response_body = r.text
        await db.commit()
        await db.refresh(rec)
        return rec
    except Exception as e:
        raise HTTPException(500, f"Recapture failed: {e}")


@router.delete("/recordings/{recording_id}", status_code=204)
async def delete_recording(recording_id: str, db: AsyncSession = Depends(get_db)):
    rec = await db.get(Recording, recording_id)
    if not rec:
        raise HTTPException(404, "Recording not found")
    from models.replay import ReplayResult
    await db.execute(
        delete(TestCaseRecording).where(TestCaseRecording.recording_id == recording_id)
    )
    await db.execute(
        delete(ReplayResult).where(ReplayResult.recording_id == recording_id)
    )
    await db.delete(rec)
    await db.commit()
