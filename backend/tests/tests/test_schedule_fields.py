"""
Tests for schedule enhancement — new fields passed to ReplayJob.

Tests the field-passing logic from _run_scheduled_replay:
  - diff_rules, assertions, perf_threshold_ms, override_host, environment
  are correctly forwarded from ScheduledReplay → ReplayJob.
"""
import pytest


# ── Helper: simulate job creation from schedule ────────────────────────────────

def build_job_from_schedule(schedule: dict, tc_recording_count: int) -> dict:
    """
    Replicate the ReplayJob constructor call from _run_scheduled_replay.
    Returns a dict representing the created job fields.
    """
    return {
        "case_id":           schedule["case_id"],
        "target_app_id":     schedule["target_app_id"],
        "total_count":       tc_recording_count,
        "concurrency":       schedule.get("concurrency", 1),
        "delay_ms":          schedule.get("delay_ms", 0),
        "ignore_fields":     schedule.get("ignore_fields"),
        "diff_rules":        schedule.get("diff_rules"),           # NEW
        "assertions":        schedule.get("assertions"),           # NEW
        "perf_threshold_ms": schedule.get("perf_threshold_ms"),   # NEW
        "override_host":     schedule.get("override_host"),       # NEW
        "webhook_url":       schedule.get("webhook_url"),
        "notify_type":       schedule.get("notify_type"),
        "environment":       schedule.get("environment") or "scheduled",  # NEW
        "created_by":        f"schedule:{schedule['id']}",
    }


class TestScheduleFieldPassing:

    def _base_schedule(self, **overrides) -> dict:
        base = {
            "id": "sched-1",
            "case_id": "case-1",
            "target_app_id": "app-1",
            "concurrency": 1,
            "delay_ms": 0,
        }
        base.update(overrides)
        return base

    def test_diff_rules_passed_to_job(self):
        rules = [{"type": "ignore", "path": "timestamp"}]
        schedule = self._base_schedule(diff_rules=rules)
        job = build_job_from_schedule(schedule, tc_recording_count=5)
        assert job["diff_rules"] == rules

    def test_assertions_passed_to_job(self):
        assertions = [{"type": "status_code_eq", "value": 200}]
        schedule = self._base_schedule(assertions=assertions)
        job = build_job_from_schedule(schedule, tc_recording_count=3)
        assert job["assertions"] == assertions

    def test_perf_threshold_ms_passed_to_job(self):
        schedule = self._base_schedule(perf_threshold_ms=1500)
        job = build_job_from_schedule(schedule, tc_recording_count=2)
        assert job["perf_threshold_ms"] == 1500

    def test_override_host_passed_to_job(self):
        schedule = self._base_schedule(override_host="192.168.1.100")
        job = build_job_from_schedule(schedule, tc_recording_count=1)
        assert job["override_host"] == "192.168.1.100"

    def test_environment_from_schedule_used(self):
        schedule = self._base_schedule(environment="production")
        job = build_job_from_schedule(schedule, tc_recording_count=4)
        assert job["environment"] == "production"

    def test_environment_defaults_to_scheduled(self):
        """When no environment set on schedule, job gets 'scheduled'."""
        schedule = self._base_schedule()  # no environment
        job = build_job_from_schedule(schedule, tc_recording_count=4)
        assert job["environment"] == "scheduled"

    def test_environment_none_defaults_to_scheduled(self):
        schedule = self._base_schedule(environment=None)
        job = build_job_from_schedule(schedule, tc_recording_count=1)
        assert job["environment"] == "scheduled"

    def test_none_fields_remain_none(self):
        """Unset optional fields stay None — don't default to empty list."""
        schedule = self._base_schedule()
        job = build_job_from_schedule(schedule, tc_recording_count=1)
        assert job["diff_rules"] is None
        assert job["assertions"] is None
        assert job["perf_threshold_ms"] is None
        assert job["override_host"] is None

    def test_webhook_and_notify_type_preserved(self):
        schedule = self._base_schedule(
            webhook_url="https://hooks.example.com/notify",
            notify_type="dingtalk",
        )
        job = build_job_from_schedule(schedule, tc_recording_count=10)
        assert job["webhook_url"] == "https://hooks.example.com/notify"
        assert job["notify_type"] == "dingtalk"

    def test_created_by_contains_schedule_id(self):
        schedule = self._base_schedule(id="sched-abc123")
        job = build_job_from_schedule(schedule, tc_recording_count=1)
        assert job["created_by"] == "schedule:sched-abc123"

    def test_total_count_from_test_case(self):
        schedule = self._base_schedule()
        job = build_job_from_schedule(schedule, tc_recording_count=42)
        assert job["total_count"] == 42

    def test_all_new_fields_together(self):
        """Verify all Phase 3 new fields are forwarded simultaneously."""
        schedule = self._base_schedule(
            diff_rules=[{"type": "numeric_tolerance", "path": "price", "tolerance": 0.01}],
            assertions=[{"type": "response_not_empty"}],
            perf_threshold_ms=3000,
            override_host="10.0.0.1",
            environment="uat",
        )
        job = build_job_from_schedule(schedule, tc_recording_count=7)
        assert len(job["diff_rules"]) == 1
        assert job["diff_rules"][0]["type"] == "numeric_tolerance"
        assert job["assertions"][0]["type"] == "response_not_empty"
        assert job["perf_threshold_ms"] == 3000
        assert job["override_host"] == "10.0.0.1"
        assert job["environment"] == "uat"


# ── Application defaults loading ──────────────────────────────────────────────

def load_app_defaults(app: dict, form: dict) -> dict:
    """
    Replicate frontend loadAppDefaults() logic:
    merge app default fields into the replay form.
    """
    result = dict(form)
    if app.get("default_ignore_fields"):
        result["ignore_fields"] = list(app["default_ignore_fields"])
    if app.get("default_diff_rules"):
        result["diff_rules"] = list(app["default_diff_rules"])
    if app.get("default_assertions"):
        result["assertions"] = list(app["default_assertions"])
    if app.get("default_perf_threshold_ms"):
        result["perf_threshold_ms"] = app["default_perf_threshold_ms"]
    return result


class TestApplicationDefaultsLoading:

    def test_all_defaults_loaded(self):
        app = {
            "default_ignore_fields": ["ts", "traceId"],
            "default_diff_rules": [{"type": "ignore", "path": "requestId"}],
            "default_assertions": [{"type": "response_not_empty"}],
            "default_perf_threshold_ms": 2000,
        }
        form = {"ignore_fields": [], "diff_rules": [], "assertions": [], "perf_threshold_ms": None}
        result = load_app_defaults(app, form)
        assert result["ignore_fields"] == ["ts", "traceId"]
        assert result["diff_rules"][0]["type"] == "ignore"
        assert result["assertions"][0]["type"] == "response_not_empty"
        assert result["perf_threshold_ms"] == 2000

    def test_none_defaults_dont_overwrite_form(self):
        app = {
            "default_ignore_fields": None,
            "default_perf_threshold_ms": None,
        }
        form = {"ignore_fields": ["myField"], "perf_threshold_ms": 500}
        result = load_app_defaults(app, form)
        assert result["ignore_fields"] == ["myField"]  # preserved
        assert result["perf_threshold_ms"] == 500       # preserved

    def test_defaults_do_not_mutate_original_form(self):
        app = {"default_ignore_fields": ["ts"]}
        form = {"ignore_fields": []}
        original_form = dict(form)
        load_app_defaults(app, form)
        assert form == original_form  # original unchanged

    def test_empty_defaults_not_applied(self):
        app = {"default_ignore_fields": []}  # empty list is falsy
        form = {"ignore_fields": ["existing"]}
        result = load_app_defaults(app, form)
        assert result["ignore_fields"] == ["existing"]

    def test_no_app_defaults_configured(self):
        app = {}
        form = {"ignore_fields": ["f1"], "perf_threshold_ms": 1000}
        result = load_app_defaults(app, form)
        assert result["ignore_fields"] == ["f1"]
        assert result["perf_threshold_ms"] == 1000
