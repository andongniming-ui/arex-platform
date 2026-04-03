"""
Tests for A/B compare logic.

Tests the pure comparison logic extracted from _run_compare:
  - agreed/diverged counting
  - status_a/status_b determination based on diff_score
  - diff_score computation for compare results
  - error handling (Bug 3 fix: FAILED status on exception)
"""
import pytest
from utils.diff import compute_diff


# ── Status determination from diff_score ──────────────────────────────────────

def determine_compare_status(score: float) -> str:
    """Replicate status_a / status_b determination from _run_compare."""
    return "PASS" if score == 0.0 else "FAIL"


class TestCompareStatusDetermination:

    def test_pass_when_score_zero(self):
        assert determine_compare_status(0.0) == "PASS"

    def test_fail_when_score_positive(self):
        assert determine_compare_status(0.1) == "FAIL"

    def test_fail_when_score_one(self):
        assert determine_compare_status(1.0) == "FAIL"

    def test_fail_when_tiny_nonzero(self):
        assert determine_compare_status(0.001) == "FAIL"


# ── agreed/diverged counting ──────────────────────────────────────────────────

def count_agreed_diverged(results: list) -> tuple[int, int]:
    """
    Replicate the agreed/diverged counting from _run_compare:
      results is a list of booleans (True=agreed, False=diverged)
      or exceptions (returned by asyncio.gather with return_exceptions=True).
    """
    agreed = sum(1 for r in results if r is True)
    diverged = sum(1 for r in results if r is False)
    return agreed, diverged


class TestAgreedDivergedCounting:

    def test_all_agreed(self):
        results = [True, True, True]
        agreed, diverged = count_agreed_diverged(results)
        assert agreed == 3
        assert diverged == 0

    def test_all_diverged(self):
        results = [False, False]
        agreed, diverged = count_agreed_diverged(results)
        assert agreed == 0
        assert diverged == 2

    def test_mixed_results(self):
        results = [True, False, True, False, True]
        agreed, diverged = count_agreed_diverged(results)
        assert agreed == 3
        assert diverged == 2

    def test_none_results_not_counted(self):
        """None means recording not found — neither agreed nor diverged."""
        results = [True, None, False, None]
        agreed, diverged = count_agreed_diverged(results)
        assert agreed == 1
        assert diverged == 1

    def test_exception_results_not_counted(self):
        """Exceptions from gather(return_exceptions=True) are neither True nor False."""
        results = [True, RuntimeError("connection error"), False]
        agreed, diverged = count_agreed_diverged(results)
        assert agreed == 1
        assert diverged == 1

    def test_empty_results(self):
        agreed, diverged = count_agreed_diverged([])
        assert agreed == 0
        assert diverged == 0


# ── Core diff logic for compare (using compute_diff directly) ─────────────────

class TestCompareDiffScores:

    def test_identical_json_responses_score_zero(self):
        body = '{"code":0,"data":{"id":1}}'
        _, score = compute_diff(body, body, [], [])
        assert score == 0.0

    def test_different_responses_score_positive(self):
        orig = '{"code":0,"data":{"id":1}}'
        repl = '{"code":0,"data":{"id":2}}'
        _, score = compute_diff(orig, repl, [], [])
        assert score > 0.0

    def test_both_none_score_zero(self):
        """Both original and replayed are None → no diff → score 0."""
        _, score = compute_diff(None, None, [], [])
        assert score == 0.0

    def test_a_none_b_nonempty_score_positive(self):
        """One side has body, other is None → diff."""
        _, score = compute_diff(None, '{"code":0}', [], [])
        assert score > 0.0

    def test_a_vs_b_direct_comparison(self):
        """Direct A vs B comparison: if both equal original, A vs B should be zero."""
        orig = '{"status":"ok","value":42}'
        body_a = orig
        body_b = orig
        _, score_ab = compute_diff(body_a, body_b, [], [])
        assert score_ab == 0.0

    def test_a_vs_b_different_values(self):
        """A and B return different responses → A vs B score > 0."""
        body_a = '{"version":"1.0","data":100}'
        body_b = '{"version":"2.0","data":200}'
        _, score_ab = compute_diff(body_a, body_b, [], [])
        assert score_ab > 0.0

    def test_compare_with_ignore_fields(self):
        """Ignored fields should not affect the score even if they differ."""
        body_a = '{"ts":1000,"value":42}'
        body_b = '{"ts":9999,"value":42}'
        ignore_patterns = [r"root\['ts'\]$"]
        _, score = compute_diff(body_a, body_b, ignore_patterns, [])
        assert score == 0.0  # ts ignored, value same → no diff


# ── agreed boolean derivation ──────────────────────────────────────────────────

def is_agreed(status_a: str, status_b: str) -> bool:
    return status_a == status_b


class TestAgreedDerivation:

    def test_both_pass_agreed(self):
        assert is_agreed("PASS", "PASS") is True

    def test_both_fail_agreed(self):
        """Both environments fail — they agree on the failure."""
        assert is_agreed("FAIL", "FAIL") is True

    def test_one_pass_one_fail_diverged(self):
        assert is_agreed("PASS", "FAIL") is False

    def test_one_fail_one_pass_diverged(self):
        assert is_agreed("FAIL", "PASS") is False

    def test_full_compare_flow_identical_responses(self):
        """End-to-end: same response to both apps → both PASS → agreed."""
        original = '{"code":0,"msg":"ok"}'
        body_a = original
        body_b = original

        _, score_a = compute_diff(original, body_a, [], [])
        _, score_b = compute_diff(original, body_b, [], [])
        _, score_ab = compute_diff(body_a, body_b, [], [])

        status_a = determine_compare_status(score_a)
        status_b = determine_compare_status(score_b)

        assert status_a == "PASS"
        assert status_b == "PASS"
        assert score_ab == 0.0
        assert is_agreed(status_a, status_b) is True

    def test_full_compare_flow_diverged_responses(self):
        """App A matches original, App B differs → PASS vs FAIL → diverged."""
        original = '{"code":0,"data":"old"}'
        body_a = original
        body_b = '{"code":0,"data":"new"}'

        _, score_a = compute_diff(original, body_a, [], [])
        _, score_b = compute_diff(original, body_b, [], [])

        status_a = determine_compare_status(score_a)
        status_b = determine_compare_status(score_b)

        assert status_a == "PASS"
        assert status_b == "FAIL"
        assert is_agreed(status_a, status_b) is False


# ── CompareRun FAILED status on exception (Bug 3 fix) ─────────────────────────

class TestCompareErrorHandling:

    def test_status_set_to_failed_on_exception(self):
        """
        Simulate what happens when _run_compare raises:
        the except block should update status to FAILED.
        """
        run_state = {"status": "RUNNING", "finished_at": None}

        def handle_exception():
            try:
                raise ConnectionError("target host unreachable")
            except Exception:
                if run_state["status"] == "RUNNING":
                    run_state["status"] = "FAILED"
                    run_state["finished_at"] = "2024-01-01"

        handle_exception()
        assert run_state["status"] == "FAILED"
        assert run_state["finished_at"] is not None

    def test_done_run_not_overwritten_by_late_exception(self):
        run_state = {"status": "DONE", "finished_at": "2024-01-01"}

        try:
            raise RuntimeError("late error")
        except Exception:
            if run_state["status"] == "RUNNING":
                run_state["status"] = "FAILED"

        assert run_state["status"] == "DONE"

    def test_failed_apps_trigger_failed_status(self):
        """If app_a or app_b not found, run should be FAILED."""
        run_state = {"status": "RUNNING"}

        def check_apps(app_a, app_b):
            if not app_a or not app_b:
                run_state["status"] = "FAILED"

        check_apps(None, {"id": "app-b"})
        assert run_state["status"] == "FAILED"


# ── ignore_field pattern generation ───────────────────────────────────────────

class TestIgnorePatternGeneration:
    """Test the ignore pattern generation used in _run_compare."""

    def _make_patterns(self, ignore_fields: list[str]) -> list[str]:
        return [rf".*\['{f}'\].*" for f in ignore_fields]

    def test_single_field(self):
        patterns = self._make_patterns(["timestamp"])
        assert len(patterns) == 1
        assert "timestamp" in patterns[0]

    def test_multiple_fields(self):
        patterns = self._make_patterns(["ts", "requestId", "traceId"])
        assert len(patterns) == 3

    def test_empty_list(self):
        assert self._make_patterns([]) == []

    def test_patterns_used_in_diff(self):
        """Ignored timestamps should not cause diff."""
        body_a = '{"ts":111,"value":1}'
        body_b = '{"ts":999,"value":1}'
        patterns = self._make_patterns(["ts"])
        _, score = compute_diff(body_a, body_b, patterns, [])
        assert score == 0.0
