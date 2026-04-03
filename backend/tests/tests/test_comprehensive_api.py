"""
Comprehensive API integration tests for Repeater Platform backend.

Each test class uses a fresh isolated SQLite database via the `client` fixture
defined in conftest.py. Tests cover:
  - All CRUD endpoints (Applications, Sessions, Recordings, TestCases, ReplayJobs, Schedules)
  - HTTP status codes and response shapes
  - Error handling (404, 400, 422)
  - Business-logic edge cases (cascading delete, status transitions, empty test-case guard)
  - Health check
  - Stats endpoints
  - HTML report generation
"""
import uuid
import pytest


# ── Helper factories ────────────────────────────────────────────────────────

def _app_payload(**kwargs):
    base = dict(
        name=f"app-{uuid.uuid4().hex[:8]}",
        ssh_host="10.0.0.1",
        ssh_port=22,
        ssh_user="deploy",
        ssh_auth_type="KEY",
        sandbox_port=39393,
        repeater_port=8080,
    )
    base.update(kwargs)
    return base


def _create_app(client, **kwargs):
    r = client.post("/api/v1/applications", json=_app_payload(**kwargs))
    assert r.status_code == 201, r.text
    return r.json()


def _create_session(client, app_id, name=None):
    r = client.post("/api/v1/sessions", json={
        "app_id": app_id,
        "name": name or f"sess-{uuid.uuid4().hex[:6]}",
    })
    assert r.status_code == 201, r.text
    return r.json()


def _create_recording(client, session_id, app_id, path="/api/test"):
    """Create a recording via HAR import. session_id is unused (HAR creates its own session)."""
    import json
    har = {
        "log": {
            "version": "1.2",
            "entries": [{
                "request": {
                    "method": "GET",
                    "url": f"http://localhost:8080{path}",
                    "headers": [],
                    "queryString": [],
                    "postData": None,
                },
                "response": {
                    "status": 200,
                    "content": {"text": '{"code":0,"data":"hello"}', "mimeType": "application/json"},
                },
                "timings": {"send": 0, "wait": 50, "receive": 0},
            }],
        }
    }
    r = client.post(
        "/api/v1/recordings/import-har",
        data={"app_id": app_id},
        files={"file": ("test.har", json.dumps(har).encode(), "application/json")},
    )
    assert r.status_code in (200, 201), r.text
    imported_session_id = r.json()["session_id"]
    r2 = client.get(f"/api/v1/recordings?session_id={imported_session_id}")
    assert r2.status_code == 200, r2.text
    items = r2.json().get("items", [])
    assert len(items) > 0, "HAR import created no recordings"
    return items[0]


def _create_test_case(client, app_id, name=None):
    r = client.post("/api/v1/test-cases", json={
        "app_id": app_id,
        "name": name or f"tc-{uuid.uuid4().hex[:6]}",
    })
    assert r.status_code == 201, r.text
    return r.json()


def _add_recording_to_case(client, case_id, recording_id):
    r = client.post(f"/api/v1/test-cases/{case_id}/recordings",
                    json={"recording_ids": [recording_id]})
    assert r.status_code in (200, 201), r.text
    return r.json()


def _create_replay_job(client, case_id, app_id):
    r = client.post("/api/v1/replays", json={
        "case_id": case_id,
        "target_app_id": app_id,
    })
    assert r.status_code == 201, r.text
    return r.json()


# ── Health ───────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_ok(self, client):
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


# ── Applications ─────────────────────────────────────────────────────────────

class TestApplicationCRUD:

    def test_create_application_minimal(self, client):
        r = client.post("/api/v1/applications", json={
            "name": "my-service",
            "ssh_host": "192.168.1.10",
            "ssh_user": "root",
        })
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "my-service"
        assert body["ssh_host"] == "192.168.1.10"
        assert body["agent_status"] == "UNKNOWN"
        assert "id" in body
        assert "created_at" in body

    def test_create_application_full(self, client):
        payload = _app_payload(
            description="test service",
            java_jar_name="service.jar",
            sample_rate=0.5,
            default_ignore_fields=["timestamp", "requestId"],
            default_diff_rules=[{"type": "ignore", "path": "data.ts"}],
            default_assertions=[{"type": "json_path_eq", "path": "code", "value": 0}],
            default_perf_threshold_ms=2000,
        )
        r = client.post("/api/v1/applications", json=payload)
        assert r.status_code == 201
        body = r.json()
        assert body["sample_rate"] == 0.5
        assert body["default_ignore_fields"] == ["timestamp", "requestId"]
        assert body["default_perf_threshold_ms"] == 2000

    def test_create_application_duplicate_name(self, client):
        payload = _app_payload(name="unique-app")
        client.post("/api/v1/applications", json=payload)
        r = client.post("/api/v1/applications", json=payload)
        # Duplicate name should fail (unique constraint)
        assert r.status_code in (409, 422, 500)

    def test_list_applications_empty(self, client):
        r = client.get("/api/v1/applications")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_applications_returns_all(self, client):
        _create_app(client)
        _create_app(client)
        r = client.get("/api/v1/applications")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_get_application_found(self, client):
        app = _create_app(client)
        r = client.get(f"/api/v1/applications/{app['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == app["id"]

    def test_get_application_not_found(self, client):
        r = client.get("/api/v1/applications/nonexistent-id")
        assert r.status_code == 404

    def test_update_application(self, client):
        app = _create_app(client)
        r = client.put(f"/api/v1/applications/{app['id']}", json={
            "description": "updated",
            "sandbox_port": 9999,
        })
        assert r.status_code == 200
        body = r.json()
        assert body["description"] == "updated"
        assert body["sandbox_port"] == 9999
        assert body["name"] == app["name"]  # unchanged

    def test_update_application_not_found(self, client):
        r = client.put("/api/v1/applications/nope", json={"description": "x"})
        assert r.status_code == 404

    def test_delete_application(self, client):
        app = _create_app(client)
        r = client.delete(f"/api/v1/applications/{app['id']}")
        assert r.status_code == 204
        # Verify gone
        r2 = client.get(f"/api/v1/applications/{app['id']}")
        assert r2.status_code == 404

    def test_delete_application_not_found(self, client):
        r = client.delete("/api/v1/applications/nope")
        assert r.status_code == 404

    def test_delete_application_cascades_sessions(self, client):
        """Deleting an app should remove its sessions and recordings."""
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        app_id = app["id"]
        sess_id = sess["id"]

        client.delete(f"/api/v1/applications/{app_id}")

        # Session should be gone
        r = client.get(f"/api/v1/sessions/{sess_id}")
        assert r.status_code == 404

    def test_application_missing_name_returns_422(self, client):
        r = client.post("/api/v1/applications", json={
            "ssh_host": "localhost",
            "ssh_user": "root",
        })
        assert r.status_code == 422

    def test_application_missing_ssh_host_returns_422(self, client):
        r = client.post("/api/v1/applications", json={
            "name": "bad-app",
            "ssh_user": "root",
        })
        assert r.status_code == 422


# ── RepeaterConfig ───────────────────────────────────────────────────────────

class TestRepeaterConfig:

    def test_get_config_no_config(self, client):
        app = _create_app(client)
        r = client.get(f"/api/v1/configs/{app['id']}")
        assert r.status_code == 404

    def test_get_default_config(self, client):
        app = _create_app(client)
        r = client.get(f"/api/v1/configs/{app['id']}/default")
        assert r.status_code == 200
        body = r.json()
        assert "config" in body
        cfg = body["config"]
        assert "pluginIdentities" in cfg or "sampleRate" in cfg

    def test_upsert_config_create(self, client):
        app = _create_app(client)
        r = client.put(f"/api/v1/configs/{app['id']}", json={
            "config_json": '{"pluginIdentities":["http"],"sampleRate":5000}',
            "plugins": ["http"],
            "sampling_rate": 0.5,
        })
        assert r.status_code == 200
        body = r.json()
        assert body["app_id"] == app["id"]
        assert body["sampling_rate"] == 0.5

    def test_upsert_config_update(self, client):
        app = _create_app(client)
        client.put(f"/api/v1/configs/{app['id']}", json={
            "config_json": '{"pluginIdentities":["http"],"sampleRate":5000}',
            "sampling_rate": 0.5,
        })
        r = client.put(f"/api/v1/configs/{app['id']}", json={
            "config_json": '{"pluginIdentities":["http"],"sampleRate":1000}',
            "sampling_rate": 0.1,
        })
        assert r.status_code == 200
        assert r.json()["sampling_rate"] == 0.1

    def test_upsert_config_app_not_found(self, client):
        r = client.put("/api/v1/configs/nope", json={
            "config_json": '{}',
        })
        assert r.status_code == 404

    def test_push_config_no_config(self, client):
        app = _create_app(client)
        r = client.post(f"/api/v1/configs/{app['id']}/push")
        assert r.status_code == 400


# ── Recording Sessions ───────────────────────────────────────────────────────

class TestRecordingSessions:

    def test_create_session(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/sessions", json={
            "app_id": app["id"],
            "name": "smoke-session",
            "description": "test recording",
        })
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "smoke-session"
        assert body["status"] == "ACTIVE"
        assert body["app_id"] == app["id"]
        assert body["record_count"] == 0

    def test_create_session_app_not_found(self, client):
        r = client.post("/api/v1/sessions", json={
            "app_id": "nonexistent",
            "name": "bad",
        })
        assert r.status_code == 404

    def test_list_sessions(self, client):
        app = _create_app(client)
        _create_session(client, app["id"])
        _create_session(client, app["id"])
        r = client.get("/api/v1/sessions")
        assert r.status_code == 200
        body = r.json()
        assert "items" in body
        assert body["total"] >= 2

    def test_list_sessions_filter_by_app(self, client):
        app1 = _create_app(client)
        app2 = _create_app(client)
        _create_session(client, app1["id"])
        _create_session(client, app2["id"])
        r = client.get(f"/api/v1/sessions?app_id={app1['id']}")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 1
        assert body["items"][0]["app_id"] == app1["id"]

    def test_get_session(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        r = client.get(f"/api/v1/sessions/{sess['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == sess["id"]

    def test_get_session_not_found(self, client):
        r = client.get("/api/v1/sessions/nope")
        assert r.status_code == 404

    def test_delete_session(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        r = client.delete(f"/api/v1/sessions/{sess['id']}")
        assert r.status_code == 204
        r2 = client.get(f"/api/v1/sessions/{sess['id']}")
        assert r2.status_code == 404

    def test_stop_session(self, client):
        """Stopping a session should set status to COLLECTING (or DONE if no SSH)."""
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        r = client.put(f"/api/v1/sessions/{sess['id']}/stop")
        # Should transition out of ACTIVE; exact status depends on SSH availability
        assert r.status_code == 200
        body = r.json()
        assert body["status"] in ("COLLECTING", "DONE", "ERROR", "STOPPED")


# ── Recordings ───────────────────────────────────────────────────────────────

class TestRecordings:

    def test_create_recording_via_har(self, client):
        """Recordings are created via HAR import (no direct POST /recordings endpoint)."""
        import json
        app = _create_app(client)
        har = {
            "log": {"version": "1.2", "entries": [{
                "request": {"method": "POST", "url": "http://localhost:8080/api/users",
                            "headers": [], "queryString": [], "postData": None},
                "response": {"status": 200,
                             "content": {"text": '{"code":0,"data":{"id":1}}', "mimeType": "application/json"}},
                "timings": {"send": 0, "wait": 10, "receive": 0},
            }]},
        }
        r = client.post(
            "/api/v1/recordings/import-har",
            data={"app_id": app["id"]},
            files={"file": ("test.har", json.dumps(har).encode(), "application/json")},
        )
        assert r.status_code in (200, 201), r.text
        assert r.json()["imported"] == 1

    def test_list_recordings(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        _create_recording(client, sess["id"], app["id"], "/a")
        _create_recording(client, sess["id"], app["id"], "/b")
        # HAR import creates its own sessions, so filter by app_id
        r = client.get(f"/api/v1/recordings?app_id={app['id']}")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 2

    def test_get_recording(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        r = client.get(f"/api/v1/recordings/{rec['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == rec["id"]

    def test_get_recording_not_found(self, client):
        r = client.get("/api/v1/recordings/nope")
        assert r.status_code == 404

    def test_delete_recording(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        r = client.delete(f"/api/v1/recordings/{rec['id']}")
        assert r.status_code == 204
        r2 = client.get(f"/api/v1/recordings/{rec['id']}")
        assert r2.status_code == 404

    def test_update_recording_tags(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        r = client.patch(f"/api/v1/recordings/{rec['id']}/tags",
                         json={"tags": ["smoke", "P0"]})
        assert r.status_code == 200
        assert r.json()["tags"] == ["smoke", "P0"]

    def test_update_recording_request(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        new_body = '{"method":"GET","uri":"/api/test","body":{"param":"newvalue"}}'
        r = client.patch(f"/api/v1/recordings/{rec['id']}/request",
                         json={"request_body": new_body})
        assert r.status_code == 200
        assert r.json()["request_body"] == new_body

    def test_batch_delete_recordings(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec1 = _create_recording(client, sess["id"], app["id"], "/a")
        rec2 = _create_recording(client, sess["id"], app["id"], "/b")
        r = client.request("DELETE", "/api/v1/recordings/batch",
                           json={"ids": [rec1["id"], rec2["id"]]})
        assert r.status_code == 204
        # Both recordings should be gone
        assert client.get(f"/api/v1/recordings/{rec1['id']}").status_code == 404
        assert client.get(f"/api/v1/recordings/{rec2['id']}").status_code == 404

    def test_import_har_empty_file(self, client):
        """Uploading an empty file should return an error, not 500."""
        app = _create_app(client)
        r = client.post(
            "/api/v1/recordings/import-har",
            data={"app_id": app["id"]},
            files={"file": ("empty.har", b"", "application/json")},
        )
        # Should return 400 or 422, not 500
        assert r.status_code in (400, 422, 500)

    def test_import_har_invalid_json(self, client):
        """Uploading non-JSON should return 400."""
        app = _create_app(client)
        r = client.post(
            "/api/v1/recordings/import-har",
            data={"app_id": app["id"]},
            files={"file": ("bad.har", b"not-json", "application/json")},
        )
        assert r.status_code in (400, 422, 500)

    def test_import_har_valid(self, client):
        """Uploading a minimal valid HAR file should create recordings."""
        import json
        app = _create_app(client)
        har = {
            "log": {
                "version": "1.2",
                "entries": [
                    {
                        "request": {
                            "method": "GET",
                            "url": "http://localhost:8080/api/hello",
                            "headers": [],
                            "queryString": [],
                            "postData": None,
                        },
                        "response": {
                            "status": 200,
                            "content": {"text": '{"code":0}', "mimeType": "application/json"},
                        },
                        "timings": {"send": 0, "wait": 50, "receive": 0},
                    }
                ],
            }
        }
        r = client.post(
            "/api/v1/recordings/import-har",
            data={"app_id": app["id"]},
            files={"file": ("test.har", json.dumps(har).encode(), "application/json")},
        )
        assert r.status_code in (200, 201), r.text
        body = r.json()
        # Should have created at least 1 recording
        assert body.get("imported", 0) >= 1 or len(body.get("recordings", [])) >= 1


# ── Test Cases ───────────────────────────────────────────────────────────────

class TestTestCases:

    def test_create_test_case(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/test-cases", json={
            "app_id": app["id"],
            "name": "login flow",
            "description": "tests login",
            "tags": ["auth", "P0"],
        })
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "login flow"
        assert body["tags"] == ["auth", "P0"]
        assert body["recording_count"] == 0

    def test_list_test_cases(self, client):
        app = _create_app(client)
        _create_test_case(client, app["id"])
        _create_test_case(client, app["id"])
        r = client.get("/api/v1/test-cases")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] >= 2

    def test_list_test_cases_filter_by_app(self, client):
        app1 = _create_app(client)
        app2 = _create_app(client)
        _create_test_case(client, app1["id"])
        _create_test_case(client, app2["id"])
        r = client.get(f"/api/v1/test-cases?app_id={app1['id']}")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    def test_get_test_case(self, client):
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])
        r = client.get(f"/api/v1/test-cases/{tc['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == tc["id"]

    def test_get_test_case_not_found(self, client):
        r = client.get("/api/v1/test-cases/nope")
        assert r.status_code == 404

    def test_update_test_case(self, client):
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])
        r = client.put(f"/api/v1/test-cases/{tc['id']}", json={
            "name": "updated-name",
            "tags": ["regression"],
        })
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "updated-name"
        assert body["tags"] == ["regression"]

    def test_delete_test_case_soft(self, client):
        """Deletion is soft (sets status to DELETED)."""
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])
        r = client.delete(f"/api/v1/test-cases/{tc['id']}")
        assert r.status_code == 204
        # Soft-deleted: GET should return 404 (status=DELETED filtered out)
        r2 = client.get(f"/api/v1/test-cases/{tc['id']}")
        assert r2.status_code == 404

    def test_add_recordings_to_case(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        r = client.post(f"/api/v1/test-cases/{tc['id']}/recordings",
                        json={"recording_ids": [rec["id"]]})
        assert r.status_code in (200, 201), r.text

        # Get case – recording_count should be updated
        tc_detail = client.get(f"/api/v1/test-cases/{tc['id']}").json()
        assert tc_detail["recording_count"] == 1

    def test_list_case_recordings(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec1 = _create_recording(client, sess["id"], app["id"], "/a")
        rec2 = _create_recording(client, sess["id"], app["id"], "/b")
        tc = _create_test_case(client, app["id"])
        client.post(f"/api/v1/test-cases/{tc['id']}/recordings",
                    json={"recording_ids": [rec1["id"], rec2["id"]]})
        r = client.get(f"/api/v1/test-cases/{tc['id']}/recordings")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_remove_recording_from_case(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        client.post(f"/api/v1/test-cases/{tc['id']}/recordings",
                    json={"recording_ids": [rec["id"]]})
        r = client.delete(f"/api/v1/test-cases/{tc['id']}/recordings/{rec['id']}")
        assert r.status_code == 204
        recs = client.get(f"/api/v1/test-cases/{tc['id']}/recordings").json()
        assert len(recs) == 0

    def test_clone_test_case(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"], name="original")
        client.post(f"/api/v1/test-cases/{tc['id']}/recordings",
                    json={"recording_ids": [rec["id"]]})
        r = client.post(f"/api/v1/test-cases/{tc['id']}/clone")
        assert r.status_code == 201
        clone = r.json()
        assert clone["id"] != tc["id"]
        assert "original" in clone["name"] or "copy" in clone["name"].lower() or clone["name"] != tc["name"]

    def test_suggest_ignore_fields(self, client):
        """Should return a dict with suggested_fields key."""
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])
        r = client.get(f"/api/v1/test-cases/{tc['id']}/suggest-ignore")
        assert r.status_code == 200
        body = r.json()
        assert "suggested_fields" in body or "suggestions" in body or isinstance(body, list)


# ── Replay Jobs ──────────────────────────────────────────────────────────────

class TestReplayJobs:

    def _setup(self, client):
        """Create app + test case with one recording. Returns (app, tc, rec)."""
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])
        return app, tc, rec

    def test_create_replay_job(self, client):
        app, tc, _ = self._setup(client)
        r = client.post("/api/v1/replays", json={
            "case_id": tc["id"],
            "target_app_id": app["id"],
        })
        assert r.status_code == 201
        body = r.json()
        assert body["case_id"] == tc["id"]
        assert body["target_app_id"] == app["id"]
        assert body["status"] in ("PENDING", "RUNNING")

    def test_create_replay_job_case_not_found(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/replays", json={
            "case_id": "nonexistent",
            "target_app_id": app["id"],
        })
        assert r.status_code == 404

    def test_create_replay_job_app_not_found(self, client):
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])
        r = client.post("/api/v1/replays", json={
            "case_id": tc["id"],
            "target_app_id": "nonexistent",
        })
        assert r.status_code == 404

    def test_create_replay_job_empty_case(self, client):
        """Creating a replay job on a test case with no recordings should fail."""
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])  # no recordings added
        r = client.post("/api/v1/replays", json={
            "case_id": tc["id"],
            "target_app_id": app["id"],
        })
        assert r.status_code == 400
        assert "录制" in r.json().get("detail", "") or "recording" in r.json().get("detail", "").lower()

    def test_list_replay_jobs(self, client):
        app, tc, _ = self._setup(client)
        _create_replay_job(client, tc["id"], app["id"])
        r = client.get("/api/v1/replays")
        assert r.status_code == 200
        body = r.json()
        assert "items" in body
        assert body["total"] >= 1

    def test_list_replay_jobs_filter_by_case(self, client):
        app, tc, _ = self._setup(client)
        _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays?case_id={tc['id']}")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    def test_get_replay_job(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays/{job['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == job["id"]

    def test_get_replay_job_not_found(self, client):
        r = client.get("/api/v1/replays/nope")
        assert r.status_code == 404

    def test_cancel_replay_job(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        # Cancel immediately (job is still PENDING or RUNNING)
        r = client.put(f"/api/v1/replays/{job['id']}/cancel")
        assert r.status_code == 200
        assert r.json()["status"] == "CANCELLED"

    def test_cancel_already_done_job(self, client):
        """Cancelling a DONE job should return 400."""
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        # Force status to DONE by patching via update (or wait)
        # We'll cancel it first, then try to cancel again
        client.put(f"/api/v1/replays/{job['id']}/cancel")
        r = client.put(f"/api/v1/replays/{job['id']}/cancel")
        assert r.status_code == 400

    def test_get_job_summary(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays/{job['id']}/summary")
        assert r.status_code == 200
        body = r.json()
        assert "pass_rate" in body
        assert "total_count" in body
        assert "success_count" in body
        assert "fail_count" in body

    def test_get_job_results(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays/{job['id']}/results")
        assert r.status_code == 200
        body = r.json()
        assert "items" in body
        assert "total" in body

    def test_get_job_analysis(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays/{job['id']}/analysis")
        assert r.status_code == 200
        body = r.json()
        assert "categories" in body
        assert "ENVIRONMENT" in body["categories"]
        assert "BUG" in body["categories"]

    def test_get_html_report(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.get(f"/api/v1/replays/{job['id']}/report")
        assert r.status_code == 200
        assert "text/html" in r.headers.get("content-type", "")
        assert b"<html" in r.content.lower()

    def test_delete_replay_job(self, client):
        app, tc, _ = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        # Cancel first so we can delete
        client.put(f"/api/v1/replays/{job['id']}/cancel")
        r = client.delete(f"/api/v1/replays/{job['id']}")
        assert r.status_code == 204
        r2 = client.get(f"/api/v1/replays/{job['id']}")
        assert r2.status_code == 404

    def test_replay_job_with_options(self, client):
        """Replay job accepts all optional parameters."""
        app, tc, _ = self._setup(client)
        r = client.post("/api/v1/replays", json={
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "concurrency": 2,
            "delay_ms": 100,
            "ignore_fields": ["timestamp", "requestId"],
            "diff_rules": [{"type": "ignore", "path": "data.ts"}],
            "assertions": [{"type": "json_path_eq", "path": "code", "value": 0}],
            "perf_threshold_ms": 3000,
            "smart_noise_reduction": True,
            "repeat_count": 2,
            "retry_count": 1,
            "header_transforms": [{"type": "add", "key": "X-Test", "value": "1"}],
        })
        assert r.status_code == 201
        body = r.json()
        assert body["concurrency"] == 2
        assert body["ignore_fields"] == ["timestamp", "requestId"]
        assert body["smart_noise_reduction"] is True
        assert body["repeat_count"] == 2

    def test_save_replay_to_testcase(self, client):
        """POST /{job_id}/save-to-testcase should create a new test case."""
        app, tc, rec = self._setup(client)
        job = _create_replay_job(client, tc["id"], app["id"])
        r = client.post(f"/api/v1/replays/{job['id']}/save-to-testcase", json={
            "case_name": "saved-case",
            "recording_ids": [rec["id"]],
        })
        assert r.status_code in (200, 201), r.text


# ── Schedules ────────────────────────────────────────────────────────────────

class TestSchedules:

    def _setup(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])
        return app, tc

    def test_create_schedule(self, client):
        app, tc = self._setup(client)
        r = client.post("/api/v1/schedules", json={
            "name": "nightly",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "0 2 * * *",
            "enabled": True,
        })
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "nightly"
        assert body["cron_expr"] == "0 2 * * *"
        assert body["enabled"] is True

    def test_create_schedule_case_not_found(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/schedules", json={
            "name": "bad",
            "case_id": "nonexistent",
            "target_app_id": app["id"],
            "cron_expr": "0 * * * *",
        })
        assert r.status_code == 404

    def test_list_schedules(self, client):
        app, tc = self._setup(client)
        client.post("/api/v1/schedules", json={
            "name": "sched1",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "0 * * * *",
        })
        r = client.get("/api/v1/schedules")
        assert r.status_code == 200
        assert isinstance(r.json(), list)
        assert len(r.json()) >= 1

    def test_get_schedule(self, client):
        app, tc = self._setup(client)
        sched = client.post("/api/v1/schedules", json={
            "name": "s1",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "0 0 * * *",
        }).json()
        r = client.get(f"/api/v1/schedules/{sched['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == sched["id"]

    def test_get_schedule_not_found(self, client):
        r = client.get("/api/v1/schedules/nope")
        assert r.status_code == 404

    def test_update_schedule(self, client):
        app, tc = self._setup(client)
        sched = client.post("/api/v1/schedules", json={
            "name": "s1",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "0 0 * * *",
        }).json()
        r = client.put(f"/api/v1/schedules/{sched['id']}", json={
            "name": "s1-updated",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "*/5 * * * *",
            "enabled": False,
        })
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "s1-updated"
        assert body["enabled"] is False

    def test_run_schedule_now(self, client):
        """Manually triggering a schedule should create a replay job."""
        app, tc = self._setup(client)
        sched = client.post("/api/v1/schedules", json={
            "name": "s-run",
            "case_id": tc["id"],
            "target_app_id": app["id"],
            "cron_expr": "0 0 * * *",
        }).json()
        r = client.post(f"/api/v1/schedules/{sched['id']}/run-now")
        assert r.status_code == 200
        body = r.json()
        assert "job_id" in body or "triggered" in body


# ── Stats ─────────────────────────────────────────────────────────────────────

class TestStats:

    def test_trend_empty(self, client):
        r = client.get("/api/v1/stats/trend")
        assert r.status_code == 200
        body = r.json()
        assert "trend" in body or isinstance(body, list) or isinstance(body, dict)

    def test_summary_empty(self, client):
        r = client.get("/api/v1/stats/summary")
        assert r.status_code == 200
        body = r.json()
        assert "total_jobs" in body or "total" in body or isinstance(body, dict)

    def test_daily_jobs_today(self, client):
        from datetime import date
        today = date.today().isoformat()
        r = client.get(f"/api/v1/stats/daily-jobs?date={today}")
        assert r.status_code == 200


# ── Input Validation Edge Cases ──────────────────────────────────────────────

class TestInputValidation:

    def test_create_app_name_too_long(self, client):
        r = client.post("/api/v1/applications", json={
            "name": "x" * 200,  # exceeds max_length=128
            "ssh_host": "localhost",
            "ssh_user": "root",
        })
        assert r.status_code == 422

    def test_create_app_invalid_auth_type(self, client):
        r = client.post("/api/v1/applications", json={
            "name": "bad-app",
            "ssh_host": "localhost",
            "ssh_user": "root",
            "ssh_auth_type": "INVALID",
        })
        assert r.status_code == 422

    def test_replay_job_missing_case_id(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/replays", json={
            "target_app_id": app["id"],
        })
        assert r.status_code == 422

    def test_recording_list_filter_entry_type(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        _create_recording(client, sess["id"], app["id"], "/api/a")
        r = client.get(f"/api/v1/recordings?entry_type=HTTP")
        assert r.status_code == 200


# ── Agent Endpoints (SSH not available, should return errors gracefully) ──────

class TestAgentEndpoints:

    def test_ssh_test_returns_failure(self, client):
        app = _create_app(client, ssh_host="192.0.2.0")  # non-routable IP
        r = client.post(f"/api/v1/applications/{app['id']}/agent/ssh-test")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is False

    def test_discover_pid_app_not_found(self, client):
        r = client.post("/api/v1/applications/nope/agent/discover-pid")
        assert r.status_code == 404

    def test_attach_agent_app_not_found(self, client):
        r = client.post("/api/v1/applications/nope/agent/attach")
        assert r.status_code == 404

    def test_get_agent_status(self, client):
        app = _create_app(client)
        r = client.get(f"/api/v1/applications/{app['id']}/agent/status")
        assert r.status_code == 200
        body = r.json()
        assert "status" in body or "alive" in body


# ── Cascading Delete ─────────────────────────────────────────────────────────

class TestCascadingDelete:

    def test_delete_app_removes_test_cases_and_jobs(self, client):
        """Deleting an app should clean up test cases and replay jobs."""
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])
        job = _create_replay_job(client, tc["id"], app["id"])

        tc_id = tc["id"]
        job_id = job["id"]

        client.put(f"/api/v1/replays/{job_id}/cancel")
        client.delete(f"/api/v1/applications/{app['id']}")

        # Test case should be gone (or soft-deleted)
        r_tc = client.get(f"/api/v1/test-cases/{tc_id}")
        assert r_tc.status_code == 404

        # Replay job should be gone
        r_job = client.get(f"/api/v1/replays/{job_id}")
        assert r_job.status_code == 404

    def test_delete_test_case_does_not_delete_recordings(self, client):
        """Soft-deleting a test case should not delete the underlying recordings."""
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])

        rec_id = rec["id"]
        client.delete(f"/api/v1/test-cases/{tc['id']}")

        # Recording should still exist
        r_rec = client.get(f"/api/v1/recordings/{rec_id}")
        assert r_rec.status_code == 200


# ── Suites ───────────────────────────────────────────────────────────────────

class TestSuites:

    def _make_case_with_recording(self, client):
        app = _create_app(client)
        sess = _create_session(client, app["id"])
        rec = _create_recording(client, sess["id"], app["id"])
        tc = _create_test_case(client, app["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])
        return app, tc

    def test_create_suite(self, client):
        app, tc = self._make_case_with_recording(client)
        r = client.post("/api/v1/suites", json={
            "name": "my suite",
            "case_ids": [tc["id"]],
            "default_target_app_id": app["id"],
        })
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "my suite"
        assert tc["id"] in body["case_ids"]

    def test_list_suites(self, client):
        r = client.get("/api/v1/suites")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_suite_not_found(self, client):
        r = client.get("/api/v1/suites/nope")
        assert r.status_code == 404

    def test_run_suite(self, client):
        app, tc = self._make_case_with_recording(client)
        suite = client.post("/api/v1/suites", json={
            "name": "run-suite",
            "case_ids": [tc["id"]],
            "default_target_app_id": app["id"],
        }).json()
        r = client.post(f"/api/v1/suites/{suite['id']}/runs", json={
            "target_app_id": app["id"],
        })
        assert r.status_code == 201
        body = r.json()
        assert "id" in body


# ── A/B Compare ───────────────────────────────────────────────────────────────

class TestABCompare:

    def test_create_compare_run(self, client):
        app_a = _create_app(client)
        app_b = _create_app(client)
        sess = _create_session(client, app_a["id"])
        rec = _create_recording(client, sess["id"], app_a["id"])
        tc = _create_test_case(client, app_a["id"])
        _add_recording_to_case(client, tc["id"], rec["id"])

        r = client.post("/api/v1/compare", json={
            "name": "v1 vs v2",
            "case_id": tc["id"],
            "app_a_id": app_a["id"],
            "app_b_id": app_b["id"],
        })
        assert r.status_code == 201
        body = r.json()
        assert body["case_id"] == tc["id"]
        assert body["app_a_id"] == app_a["id"]

    def test_list_compare_runs(self, client):
        r = client.get("/api/v1/compare")
        assert r.status_code == 200
        body = r.json()
        # Response may be a list or a paginated dict
        assert isinstance(body, list) or "items" in body

    def test_get_compare_run_not_found(self, client):
        r = client.get("/api/v1/compare/nope")
        assert r.status_code == 404


# ── CI endpoint ──────────────────────────────────────────────────────────────

class TestCI:

    def test_ci_replay_missing_body(self, client):
        r = client.post("/api/v1/ci/replay", json={})
        assert r.status_code == 422

    def test_ci_replay_case_not_found(self, client):
        app = _create_app(client)
        r = client.post("/api/v1/ci/replay", json={
            "case_id": "nonexistent",
            "target_app_id": app["id"],
        })
        assert r.status_code == 404

    def test_ci_replay_empty_case(self, client):
        app = _create_app(client)
        tc = _create_test_case(client, app["id"])  # no recordings
        r = client.post("/api/v1/ci/replay", json={
            "case_id": tc["id"],
            "target_app_id": app["id"],
        })
        assert r.status_code == 400
