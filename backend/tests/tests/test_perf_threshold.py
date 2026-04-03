"""
Tests for perf_threshold_ms logic in _replay_one and assertion handling.

We test the pure business-logic parts without spinning up a real DB or HTTP server:
  - perf_threshold assertion is appended when duration > threshold (no error)
  - perf_threshold is NOT appended when error_msg is set (Bug 4 fix)
  - perf_threshold is NOT appended when duration <= threshold
  - perf_threshold causes status = FAIL
  - status = PASS when duration is within threshold and diff == 0
"""
import pytest
from utils.assertions import assertions_all_passed, evaluate_assertions


# ── helpers ────────────────────────────────────────────────────────────────────

def make_perf_result(passed: bool, duration_ms: int, threshold_ms: int) -> dict:
    return {
        "type": "perf_threshold",
        "passed": passed,
        "message": f"duration {duration_ms}ms exceeds threshold {threshold_ms}ms",
    }


def simulate_perf_check(error_msg, perf_threshold_ms, duration_ms_so_far, existing_assertion_results=None):
    """
    Replicate the fixed perf_threshold logic from _replay_one for unit testing.
    Returns updated assertion_results list.
    """
    assertion_results = list(existing_assertion_results) if existing_assertion_results else None

    # Fix Bug 4: only check perf when no error
    if not error_msg and perf_threshold_ms:
        if duration_ms_so_far > perf_threshold_ms:
            perf_result = {
                "type": "perf_threshold",
                "passed": False,
                "message": f"duration {duration_ms_so_far}ms exceeds threshold {perf_threshold_ms}ms",
            }
            assertion_results = (assertion_results or []) + [perf_result]

    return assertion_results


def determine_status(error_msg, diff_score, assertion_results):
    """Replicate status determination logic from _replay_one."""
    if error_msg:
        return "ERROR"
    elif diff_score == 0.0 and assertions_all_passed(assertion_results):
        return "PASS"
    else:
        return "FAIL"


# ── perf check logic ───────────────────────────────────────────────────────────

class TestPerfThresholdLogic:

    def test_perf_fails_when_duration_exceeds_threshold(self):
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=1000,
            duration_ms_so_far=1500,
        )
        assert results is not None
        assert len(results) == 1
        assert results[0]["type"] == "perf_threshold"
        assert results[0]["passed"] is False
        assert "1500ms" in results[0]["message"]
        assert "1000ms" in results[0]["message"]

    def test_perf_passes_when_duration_within_threshold(self):
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=1000,
            duration_ms_so_far=999,
        )
        assert results is None  # no assertion appended

    def test_perf_exactly_at_threshold_does_not_fail(self):
        """Boundary: duration == threshold should NOT fail (only strictly >)."""
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=500,
            duration_ms_so_far=500,
        )
        assert results is None

    def test_perf_check_skipped_when_error_msg_set(self):
        """Bug 4 fix: perf check must not fire when HTTP request itself failed."""
        results = simulate_perf_check(
            error_msg="Connection refused",
            perf_threshold_ms=100,
            duration_ms_so_far=9999,  # would exceed threshold
        )
        assert results is None

    def test_perf_check_skipped_when_threshold_is_none(self):
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=None,
            duration_ms_so_far=9999,
        )
        assert results is None

    def test_perf_check_skipped_when_threshold_is_zero(self):
        """Zero threshold should be treated as disabled (falsy)."""
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=0,
            duration_ms_so_far=9999,
        )
        assert results is None

    def test_perf_result_appended_to_existing_assertion_results(self):
        existing = [{"type": "status_code_eq", "passed": True, "message": "200 == 200"}]
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=500,
            duration_ms_so_far=600,
            existing_assertion_results=existing,
        )
        assert len(results) == 2
        assert results[0]["type"] == "status_code_eq"
        assert results[1]["type"] == "perf_threshold"

    def test_perf_does_not_mutate_original_list(self):
        """Original assertion list must not be mutated."""
        original = [{"type": "response_not_empty", "passed": True, "message": "ok"}]
        simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=100,
            duration_ms_so_far=200,
            existing_assertion_results=original,
        )
        assert len(original) == 1  # unchanged


# ── status determination ───────────────────────────────────────────────────────

class TestStatusDetermination:

    def test_pass_when_no_diff_no_assertions(self):
        status = determine_status(error_msg=None, diff_score=0.0, assertion_results=None)
        assert status == "PASS"

    def test_pass_when_no_diff_and_all_assertions_pass(self):
        results = [{"type": "status_code_eq", "passed": True, "message": "ok"}]
        status = determine_status(error_msg=None, diff_score=0.0, assertion_results=results)
        assert status == "PASS"

    def test_fail_when_diff_score_nonzero(self):
        status = determine_status(error_msg=None, diff_score=0.5, assertion_results=None)
        assert status == "FAIL"

    def test_fail_when_perf_assertion_fails(self):
        """Even with diff_score=0.0, a failed perf assertion makes status FAIL."""
        results = [make_perf_result(passed=False, duration_ms=2000, threshold_ms=1000)]
        status = determine_status(error_msg=None, diff_score=0.0, assertion_results=results)
        assert status == "FAIL"

    def test_error_overrides_everything(self):
        """error_msg always produces ERROR status regardless of assertions."""
        results = [make_perf_result(passed=False, duration_ms=5000, threshold_ms=100)]
        status = determine_status(
            error_msg="Connection refused",
            diff_score=0.0,
            assertion_results=results,
        )
        assert status == "ERROR"

    def test_pass_when_perf_threshold_not_exceeded(self):
        """No perf assertion appended → status can still be PASS."""
        results = simulate_perf_check(
            error_msg=None,
            perf_threshold_ms=5000,
            duration_ms_so_far=100,
        )
        status = determine_status(error_msg=None, diff_score=0.0, assertion_results=results)
        assert status == "PASS"

    def test_fail_combined_diff_and_perf(self):
        """Both diff and perf fail → FAIL."""
        results = [make_perf_result(passed=False, duration_ms=3000, threshold_ms=1000)]
        status = determine_status(error_msg=None, diff_score=0.3, assertion_results=results)
        assert status == "FAIL"


# ── assertions_all_passed with perf_threshold entries ─────────────────────────

class TestAssertionsAllPassedWithPerf:

    def test_empty_list_passes(self):
        assert assertions_all_passed([]) is True

    def test_none_passes(self):
        assert assertions_all_passed(None) is True

    def test_single_perf_fail(self):
        results = [make_perf_result(passed=False, duration_ms=2000, threshold_ms=1000)]
        assert assertions_all_passed(results) is False

    def test_mixed_pass_and_perf_fail(self):
        results = [
            {"type": "status_code_eq", "passed": True, "message": "200 == 200"},
            make_perf_result(passed=False, duration_ms=2000, threshold_ms=1000),
        ]
        assert assertions_all_passed(results) is False

    def test_all_pass_including_perf(self):
        results = [
            {"type": "status_code_eq", "passed": True, "message": "200 == 200"},
            {"type": "perf_threshold", "passed": True, "message": "300ms <= 1000ms"},
        ]
        assert assertions_all_passed(results) is True
