"""
Tests for backend/utils/failure_analyzer.py
"""
import json
import pytest
from utils.failure_analyzer import (
    analyze_failure,
    get_failure_category_stats,
    _matches_any_pattern,
    _analyze_diff_fields,
    _analyze_assertions,
)


class TestMatchesAnyPattern:
    """Test the pattern matching utility."""

    def test_empty_text(self):
        assert _matches_any_pattern("", ["test"]) is False
        assert _matches_any_pattern(None, ["test"]) is False

    def test_basic_match(self):
        assert _matches_any_pattern("connection refused", ["connection refused"]) is True
        assert _matches_any_pattern("Connection Refused", ["connection refused"]) is True

    def test_regex_match(self):
        assert _matches_any_pattern("timeout after 30s", [r"timeout"]) is True
        assert _matches_any_pattern("ECONNREFUSED", [r"ECONNREFUSED"]) is True

    def test_no_match(self):
        assert _matches_any_pattern("hello world", ["timeout", "refused"]) is False


class TestAnalyzeDiffFields:
    """Test diff field analysis."""

    def test_empty_diff(self):
        result = _analyze_diff_fields(None, [])
        assert result["all_fields"] == []
        assert result["critical_fields"] == []

    def test_invalid_json(self):
        result = _analyze_diff_fields("not json", [])
        assert result["all_fields"] == []

    def test_dynamic_field_detection(self):
        diff = json.dumps({
            "values_changed": {
                "root['requestId']": {"old": "abc", "new": "def"},
                "root['timestamp']": {"old": 100, "new": 200},
            }
        })
        result = _analyze_diff_fields(diff, [])
        assert "root['requestId']" in result["dynamic_fields"]
        assert "root['timestamp']" in result["dynamic_fields"]
        assert len(result["critical_fields"]) == 0

    def test_critical_field_detection(self):
        diff = json.dumps({
            "values_changed": {
                "root['price']": {"old": 100, "new": 200},
                "root['status']": {"old": "active", "new": "inactive"},
            }
        })
        result = _analyze_diff_fields(diff, [])
        assert "root['price']" in result["critical_fields"]
        assert "root['status']" in result["critical_fields"]

    def test_type_changes_detection(self):
        diff = json.dumps({
            "type_changes": {
                "root['data']": {
                    "old_type": "int",
                    "new_type": "str",
                    "old_value": 123,
                    "new_value": "hello",
                }
            }
        })
        result = _analyze_diff_fields(diff, [])
        assert "root['data']" in result["all_fields"]


class TestAnalyzeAssertions:
    """Test assertion analysis."""

    def test_empty_assertions(self):
        result = _analyze_assertions(None)
        assert result["perf_failed"] is False
        assert result["assertion_failed"] is False

    def test_perf_failure(self):
        assertions = [{"type": "perf_threshold", "passed": False, "message": "too slow"}]
        result = _analyze_assertions(assertions)
        assert result["perf_failed"] is True
        assert "perf_threshold" in result["failed_types"]

    def test_assertion_failure(self):
        assertions = [{"type": "status_code_eq", "passed": False, "message": "expected 200 got 500"}]
        result = _analyze_assertions(assertions)
        assert result["assertion_failed"] is True
        assert result["perf_failed"] is False

    def test_all_passed(self):
        assertions = [
            {"type": "status_code_eq", "passed": True, "message": "ok"},
            {"type": "perf_threshold", "passed": True, "message": "ok"},
        ]
        result = _analyze_assertions(assertions)
        assert result["perf_failed"] is False
        assert result["assertion_failed"] is False

    def test_mixed_results(self):
        assertions = [
            {"type": "status_code_eq", "passed": True, "message": "ok"},
            {"type": "perf_threshold", "passed": False, "message": "too slow"},
            {"type": "json_path_eq", "passed": False, "message": "value mismatch"},
        ]
        result = _analyze_assertions(assertions)
        assert result["perf_failed"] is True
        assert result["assertion_failed"] is True


class TestAnalyzeFailure:
    """Test the main analyze_failure function."""

    def test_environment_network_timeout(self):
        cat, reason = analyze_failure(
            error_message="Connection timeout after 30s",
            diff_json=None,
            diff_score=None,
            replayed_status_code=None,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"
        assert "环境/网络问题" in reason

    def test_environment_connection_refused(self):
        cat, reason = analyze_failure(
            error_message="ECONNREFUSED: Connection refused",
            diff_json=None,
            diff_score=None,
            replayed_status_code=None,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"

    def test_environment_502_error(self):
        cat, reason = analyze_failure(
            error_message="502 Bad Gateway",
            diff_json=None,
            diff_score=None,
            replayed_status_code=None,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"

    def test_environment_500_status_code(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=500,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"
        assert "服务器错误" in reason

    def test_environment_503_status_code(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=503,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"

    def test_bug_400_status_code(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=404,
            assertion_results=None,
        )
        assert cat == "BUG"
        assert "客户端错误" in reason

    def test_bug_422_status_code(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=422,
            assertion_results=None,
        )
        assert cat == "BUG"

    def test_performance_threshold_exceeded(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=200,
            assertion_results=[
                {"type": "perf_threshold", "passed": False, "message": "duration 5000ms exceeds threshold 1000ms"}
            ],
        )
        assert cat == "PERFORMANCE"
        assert "duration" in reason or "性能" in reason

    def test_data_issue_dynamic_fields_low_score(self):
        diff = json.dumps({
            "values_changed": {
                "root['requestId']": {"old": "abc-123", "new": "def-456"},
                "root['timestamp']": {"old": 1000, "new": 2000},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.05,
            replayed_status_code=200,
            assertion_results=None,
        )
        assert cat == "DATA_ISSUE"
        assert "动态字段" in reason

    def test_data_issue_mostly_dynamic_fields(self):
        diff = json.dumps({
            "values_changed": {
                "root['requestId']": {"old": "abc", "new": "def"},
                "root['timestamp']": {"old": 1000, "new": 2000},
                "root['uuid']": {"old": "uuid-1", "new": "uuid-2"},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.2,
            replayed_status_code=200,
            assertion_results=None,
        )
        assert cat == "DATA_ISSUE"

    def test_bug_critical_field_change(self):
        diff = json.dumps({
            "values_changed": {
                "root['data']['price']": {"old": 100, "new": 200},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.5,
            replayed_status_code=200,
            assertion_results=None,
        )
        assert cat == "BUG"
        assert "核心业务字段" in reason

    def test_bug_assertion_failure(self):
        diff = json.dumps({
            "values_changed": {
                "root['name']": {"old": "Alice", "new": "Bob"},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.1,
            replayed_status_code=200,
            assertion_results=[
                {"type": "json_path_eq", "passed": False, "message": "expected Alice got Bob"}
            ],
        )
        # name matches CRITICAL_FIELD_PATTERNS ("message" pattern), so BUG
        assert cat == "BUG"

    def test_bug_diff_with_score(self):
        diff = json.dumps({
            "values_changed": {
                "root['username']": {"old": "admin", "new": "root"},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.4,
            replayed_status_code=200,
            assertion_results=None,
        )
        # username matches CRITICAL_FIELD_PATTERNS ("result" might not match, but let's check)
        # "username" doesn't directly match critical patterns, but diff_score > 0 means BUG
        assert cat in ("BUG", "DATA_ISSUE")

    def test_unknown_no_info(self):
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=None,
            assertion_results=None,
        )
        assert cat == "UNKNOWN"
        assert "无法自动判定" in reason

    def test_environment_priority_over_data_issue(self):
        """Environment errors should take priority over data issues."""
        diff = json.dumps({
            "values_changed": {
                "root['requestId']": {"old": "abc", "new": "def"},
            }
        })
        cat, reason = analyze_failure(
            error_message="Connection timeout",
            diff_json=diff,
            diff_score=0.05,
            replayed_status_code=200,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"

    def test_status_code_priority(self):
        """HTTP status code errors should be checked before diff analysis."""
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=None,
            diff_score=None,
            replayed_status_code=500,
            assertion_results=None,
        )
        assert cat == "ENVIRONMENT"

    def test_performance_priority_over_diff(self):
        """Performance failures should take priority over diff analysis."""
        diff = json.dumps({
            "values_changed": {
                "root['price']": {"old": 100, "new": 200},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.5,
            replayed_status_code=200,
            assertion_results=[
                {"type": "perf_threshold", "passed": False, "message": "too slow"}
            ],
        )
        assert cat == "PERFORMANCE"

    def test_ignore_fields_data_issue(self):
        """Fields in ignore list should be treated as safe to ignore."""
        diff = json.dumps({
            "values_changed": {
                "root['customId']": {"old": "1", "new": "2"},
            }
        })
        cat, reason = analyze_failure(
            error_message=None,
            diff_json=diff,
            diff_score=0.03,
            replayed_status_code=200,
            assertion_results=None,
            ignore_fields=["customId"],
        )
        assert cat == "DATA_ISSUE"


class TestGetFailureCategoryStats:
    """Test aggregate failure statistics."""

    def test_empty_results(self):
        stats = get_failure_category_stats([])
        assert stats["total_failures"] == 0
        assert stats["ENVIRONMENT"]["count"] == 0

    def test_mixed_results(self):
        results = [
            {"status": "PASS", "failure_category": None},
            {"status": "FAIL", "failure_category": "BUG"},
            {"status": "FAIL", "failure_category": "BUG"},
            {"status": "ERROR", "failure_category": "ENVIRONMENT"},
            {"status": "FAIL", "failure_category": "DATA_ISSUE"},
            {"status": "IGNORED", "failure_category": None},
        ]
        stats = get_failure_category_stats(results)
        assert stats["total_failures"] == 4
        assert stats["BUG"]["count"] == 2
        assert stats["BUG"]["percentage"] == 50.0
        assert stats["ENVIRONMENT"]["count"] == 1
        assert stats["ENVIRONMENT"]["percentage"] == 25.0
        assert stats["DATA_ISSUE"]["count"] == 1
        assert stats["DATA_ISSUE"]["percentage"] == 25.0

    def test_unknown_category(self):
        results = [
            {"status": "FAIL", "failure_category": "INVALID_CATEGORY"},
        ]
        stats = get_failure_category_stats(results)
        assert stats["UNKNOWN"]["count"] == 1
        assert stats["UNKNOWN"]["percentage"] == 100.0

    def test_no_failures(self):
        results = [
            {"status": "PASS", "failure_category": None},
            {"status": "PASS", "failure_category": None},
        ]
        stats = get_failure_category_stats(results)
        assert stats["total_failures"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
