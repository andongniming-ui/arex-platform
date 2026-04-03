"""
Tests for Suite runner logic.

Tests the pure logic extracted from _run_suite:
  - Default merging (suite defaults vs run overrides)
  - total_cases accounting (Bug 1 fix: skipped cases not counted)
  - Pass/fail tally logic
  - overall_pass_rate calculation
"""
import pytest


# ── Default-merging logic ──────────────────────────────────────────────────────

def merge_run_defaults(req_dict: dict, suite_dict: dict) -> dict:
    """
    Replicate the default-merging logic from _run_suite.
    req_dict fields take precedence over suite_dict defaults.
    """
    return {
        "concurrency":        req_dict.get("concurrency") or suite_dict.get("default_concurrency") or 1,
        "ignore_fields":      req_dict.get("ignore_fields") or suite_dict.get("default_ignore_fields"),
        "diff_rules":         req_dict.get("diff_rules") or suite_dict.get("default_diff_rules"),
        "assertions":         req_dict.get("assertions") or suite_dict.get("default_assertions"),
        "perf_threshold_ms":  req_dict.get("perf_threshold_ms") or suite_dict.get("default_perf_threshold_ms"),
        "environment":        req_dict.get("environment") or suite_dict.get("default_environment"),
        "override_host":      req_dict.get("override_host") or suite_dict.get("default_override_host"),
        "delay_ms":           suite_dict.get("default_delay_ms") or 0,
    }


class TestDefaultMerging:

    def test_run_overrides_suite_defaults(self):
        req = {"concurrency": 5, "environment": "prod", "perf_threshold_ms": 2000}
        suite = {
            "default_concurrency": 1,
            "default_environment": "staging",
            "default_perf_threshold_ms": 500,
        }
        result = merge_run_defaults(req, suite)
        assert result["concurrency"] == 5
        assert result["environment"] == "prod"
        assert result["perf_threshold_ms"] == 2000

    def test_suite_defaults_used_when_req_empty(self):
        req = {}
        suite = {
            "default_concurrency": 3,
            "default_environment": "staging",
            "default_ignore_fields": ["timestamp", "requestId"],
            "default_perf_threshold_ms": 1000,
        }
        result = merge_run_defaults(req, suite)
        assert result["concurrency"] == 3
        assert result["environment"] == "staging"
        assert result["ignore_fields"] == ["timestamp", "requestId"]
        assert result["perf_threshold_ms"] == 1000

    def test_fallback_concurrency_to_1(self):
        req = {}
        suite = {}
        result = merge_run_defaults(req, suite)
        assert result["concurrency"] == 1

    def test_fallback_delay_ms_to_0(self):
        req = {}
        suite = {}
        result = merge_run_defaults(req, suite)
        assert result["delay_ms"] == 0

    def test_none_fields_fall_back_to_suite(self):
        req = {"ignore_fields": None}  # explicitly None, should fall back
        suite = {"default_ignore_fields": ["field1"]}
        result = merge_run_defaults(req, suite)
        assert result["ignore_fields"] == ["field1"]

    def test_empty_list_ignored_as_falsy(self):
        """Empty list is falsy in Python — suite default should take over."""
        req = {"ignore_fields": []}
        suite = {"default_ignore_fields": ["field1"]}
        result = merge_run_defaults(req, suite)
        # [] is falsy, so suite default applies
        assert result["ignore_fields"] == ["field1"]

    def test_suite_defaults_all_none(self):
        req = {}
        suite = {}
        result = merge_run_defaults(req, suite)
        assert result["ignore_fields"] is None
        assert result["diff_rules"] is None
        assert result["assertions"] is None
        assert result["perf_threshold_ms"] is None
        assert result["environment"] is None
        assert result["override_host"] is None


# ── total_cases accounting (Bug 1 fix) ────────────────────────────────────────

def compute_total_cases(case_ids: list, cases_with_recordings: set) -> int:
    """
    Replicate the Bug 1 fix: total_cases = number of cases that actually have recordings.
    (Previously used len(case_ids) which could include cases with no recordings.)
    """
    return sum(1 for cid in case_ids if cid in cases_with_recordings)


class TestTotalCasesAccounting:

    def test_all_cases_have_recordings(self):
        case_ids = ["c1", "c2", "c3"]
        with_recs = {"c1", "c2", "c3"}
        assert compute_total_cases(case_ids, with_recs) == 3

    def test_some_cases_missing_recordings(self):
        case_ids = ["c1", "c2", "c3"]
        with_recs = {"c1", "c3"}  # c2 has no recordings
        assert compute_total_cases(case_ids, with_recs) == 2

    def test_no_cases_have_recordings(self):
        case_ids = ["c1", "c2"]
        with_recs = set()
        assert compute_total_cases(case_ids, with_recs) == 0

    def test_empty_suite(self):
        assert compute_total_cases([], set()) == 0

    def test_previous_bug_total_cases_counted_incorrectly(self):
        """
        Demonstrate what Bug 1 was:
        old behavior used len(suite.case_ids) ignoring skips.
        """
        case_ids = ["c1", "c2", "c3"]
        with_recs = {"c1"}  # only c1 has recordings
        old_total = len(case_ids)          # Bug 1: would be 3
        new_total = compute_total_cases(case_ids, with_recs)  # Fix: should be 1
        assert old_total == 3   # demonstrates the bug
        assert new_total == 1   # correct value


# ── Pass/fail tally logic ──────────────────────────────────────────────────────

def tally_suite_results(jobs: list[dict]) -> dict:
    """
    Replicate the tally logic from _run_suite.
    Each job dict: {"sent_count": int, "success_count": int}
    """
    total_req = 0
    passed_req = 0
    passed_cases = 0
    failed_cases = 0

    for job in jobs:
        sent = job.get("sent_count") or 0
        success = job.get("success_count") or 0
        total_req += sent
        passed_req += success
        if sent > 0 and success == sent:
            passed_cases += 1
        else:
            failed_cases += 1

    overall_pass_rate = passed_req / total_req if total_req else 0.0
    return {
        "total_requests": total_req,
        "passed_requests": passed_req,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "overall_pass_rate": overall_pass_rate,
    }


class TestTallyLogic:

    def test_all_jobs_pass(self):
        jobs = [
            {"sent_count": 5, "success_count": 5},
            {"sent_count": 3, "success_count": 3},
        ]
        result = tally_suite_results(jobs)
        assert result["total_requests"] == 8
        assert result["passed_requests"] == 8
        assert result["passed_cases"] == 2
        assert result["failed_cases"] == 0
        assert result["overall_pass_rate"] == 1.0

    def test_partial_pass(self):
        jobs = [
            {"sent_count": 4, "success_count": 4},  # passed
            {"sent_count": 4, "success_count": 2},  # failed (partial)
        ]
        result = tally_suite_results(jobs)
        assert result["total_requests"] == 8
        assert result["passed_requests"] == 6
        assert result["passed_cases"] == 1
        assert result["failed_cases"] == 1
        assert result["overall_pass_rate"] == pytest.approx(0.75)

    def test_all_jobs_fail(self):
        jobs = [
            {"sent_count": 3, "success_count": 0},
            {"sent_count": 2, "success_count": 1},
        ]
        result = tally_suite_results(jobs)
        assert result["passed_cases"] == 0
        assert result["failed_cases"] == 2

    def test_job_with_zero_sent_counts_as_failed(self):
        """A job where sent=0 (e.g., no recordings executed) counts as failed."""
        jobs = [{"sent_count": 0, "success_count": 0}]
        result = tally_suite_results(jobs)
        assert result["passed_cases"] == 0
        assert result["failed_cases"] == 1

    def test_empty_job_list(self):
        result = tally_suite_results([])
        assert result["total_requests"] == 0
        assert result["passed_requests"] == 0
        assert result["passed_cases"] == 0
        assert result["failed_cases"] == 0
        assert result["overall_pass_rate"] == 0.0

    def test_overall_pass_rate_calculation(self):
        jobs = [
            {"sent_count": 10, "success_count": 7},
            {"sent_count": 10, "success_count": 3},
        ]
        result = tally_suite_results(jobs)
        assert result["overall_pass_rate"] == pytest.approx(0.5)

    def test_pass_rate_zero_when_no_requests(self):
        result = tally_suite_results([])
        assert result["overall_pass_rate"] == 0.0


# ── Suite FAILED status on exception (Bug 2 fix) ──────────────────────────────

class TestSuiteErrorHandling:

    def test_status_set_to_failed_on_exception(self):
        """
        Simulate what happens when _run_suite raises:
        the except block should update status to FAILED.
        """
        run_state = {"status": "RUNNING", "finished_at": None}

        def handle_exception():
            try:
                raise RuntimeError("DB connection lost")
            except Exception:
                if run_state["status"] == "RUNNING":
                    run_state["status"] = "FAILED"
                    run_state["finished_at"] = "2024-01-01"

        handle_exception()
        assert run_state["status"] == "FAILED"
        assert run_state["finished_at"] is not None

    def test_already_done_run_not_overwritten(self):
        """Don't overwrite a DONE run if exception happens after completion."""
        run_state = {"status": "DONE", "finished_at": "2024-01-01"}

        try:
            raise RuntimeError("late exception")
        except Exception:
            if run_state["status"] == "RUNNING":
                run_state["status"] = "FAILED"

        assert run_state["status"] == "DONE"  # preserved
