"""
Unit tests for utils/assertions.py — evaluate_assertions and helpers.
Run: cd backend && python -m pytest tests/test_assertions.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import pytest
from utils.assertions import (
    evaluate_assertions,
    assertions_all_passed,
    _coerce_value,
    _path_exists,
    _get_path,
)


def js(obj) -> str:
    return json.dumps(obj)


# ══════════════════════════════════════════════════════════════════════════════
# 1. _coerce_value helper
# ══════════════════════════════════════════════════════════════════════════════

class TestCoerceValue:
    def test_string_integer(self):
        assert _coerce_value("200") == 200
        assert isinstance(_coerce_value("200"), int)

    def test_string_float(self):
        assert _coerce_value("0.5") == 0.5

    def test_string_bool(self):
        assert _coerce_value("true") is True
        assert _coerce_value("false") is False

    def test_string_null(self):
        assert _coerce_value("null") is None

    def test_already_int(self):
        assert _coerce_value(200) == 200

    def test_already_float(self):
        assert _coerce_value(0.5) == 0.5

    def test_plain_string_stays_string(self):
        assert _coerce_value("hello") == "hello"

    def test_none_stays_none(self):
        assert _coerce_value(None) is None


# ══════════════════════════════════════════════════════════════════════════════
# 2. _path_exists / _get_path helpers
# ══════════════════════════════════════════════════════════════════════════════

class TestPathHelpers:
    body = {"code": 0, "data": {"id": 1, "name": None}, "items": [{"price": 9.9}]}

    def test_get_top_level(self):
        assert _get_path(self.body, "code") == 0

    def test_get_nested(self):
        assert _get_path(self.body, "data.id") == 1

    def test_get_array_by_index(self):
        assert _get_path(self.body, "items.0.price") == 9.9

    def test_get_missing_returns_none(self):
        assert _get_path(self.body, "data.missing") is None

    def test_get_null_value_returns_none(self):
        # name is explicitly null → _get_path returns None
        assert _get_path(self.body, "data.name") is None

    def test_path_exists_null_value(self):
        # Key exists but value is null → should still exist
        assert _path_exists(self.body, "data.name") is True

    def test_path_exists_missing_key(self):
        assert _path_exists(self.body, "data.missing") is False

    def test_path_exists_nested(self):
        assert _path_exists(self.body, "data.id") is True

    def test_path_exists_top_level(self):
        assert _path_exists(self.body, "code") is True

    def test_path_strips_dollar(self):
        assert _get_path(self.body, "$.code") == 0


# ══════════════════════════════════════════════════════════════════════════════
# 3. status_code_eq
# ══════════════════════════════════════════════════════════════════════════════

class TestStatusCodeEq:
    def test_pass_integer_expected(self):
        results = evaluate_assertions(
            [{"type": "status_code_eq", "value": 200}],
            '{"code":0}', 200, None
        )
        assert results[0]["passed"] is True

    def test_pass_string_expected(self):
        # Frontend sends "200" as string; should still pass
        results = evaluate_assertions(
            [{"type": "status_code_eq", "value": "200"}],
            '{"code":0}', 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_wrong_status(self):
        results = evaluate_assertions(
            [{"type": "status_code_eq", "value": 200}],
            '{"error":"not found"}', 404, None
        )
        assert results[0]["passed"] is False

    def test_message_contains_actual_code(self):
        results = evaluate_assertions(
            [{"type": "status_code_eq", "value": 200}],
            None, 500, None
        )
        assert "500" in results[0]["message"]


# ══════════════════════════════════════════════════════════════════════════════
# 4. response_not_empty
# ══════════════════════════════════════════════════════════════════════════════

class TestResponseNotEmpty:
    def test_pass_non_empty(self):
        results = evaluate_assertions(
            [{"type": "response_not_empty"}],
            '{"a":1}', None, None
        )
        assert results[0]["passed"] is True

    def test_fail_none_body(self):
        results = evaluate_assertions(
            [{"type": "response_not_empty"}],
            None, 200, None
        )
        assert results[0]["passed"] is False

    def test_fail_whitespace_only(self):
        results = evaluate_assertions(
            [{"type": "response_not_empty"}],
            "   ", 200, None
        )
        assert results[0]["passed"] is False

    def test_fail_empty_string(self):
        results = evaluate_assertions(
            [{"type": "response_not_empty"}],
            "", 200, None
        )
        assert results[0]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# 5. json_path_eq
# ══════════════════════════════════════════════════════════════════════════════

class TestJsonPathEq:
    body = js({"code": 0, "msg": "ok", "data": {"count": 5}})

    def test_pass_integer_value(self):
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "code", "value": 0}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_pass_string_value_from_frontend(self):
        # Frontend sends "0" as string → should coerce to int 0
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "code", "value": "0"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_pass_string_field(self):
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "msg", "value": "ok"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_wrong_value(self):
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "code", "value": 1}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False

    def test_pass_nested_path(self):
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "data.count", "value": "5"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_missing_path(self):
        results = evaluate_assertions(
            [{"type": "json_path_eq", "path": "nonexistent", "value": 0}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# 6. json_path_contains
# ══════════════════════════════════════════════════════════════════════════════

class TestJsonPathContains:
    body = js({"message": "Operation successful", "code": 0})

    def test_pass_substring(self):
        results = evaluate_assertions(
            [{"type": "json_path_contains", "path": "message", "value": "successful"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_missing_substring(self):
        results = evaluate_assertions(
            [{"type": "json_path_contains", "path": "message", "value": "error"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False

    def test_integer_field_contains_string_of_value(self):
        # code=0, value="0" → str(0) contains "0"
        results = evaluate_assertions(
            [{"type": "json_path_contains", "path": "code", "value": "0"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True


# ══════════════════════════════════════════════════════════════════════════════
# 7. json_path_exists
# ══════════════════════════════════════════════════════════════════════════════

class TestJsonPathExists:
    body = js({"code": 0, "data": {"id": 1, "token": None}})

    def test_pass_existing_field(self):
        results = evaluate_assertions(
            [{"type": "json_path_exists", "path": "code"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_pass_null_value_field_still_exists(self):
        # token is null but the key IS present → should pass
        results = evaluate_assertions(
            [{"type": "json_path_exists", "path": "data.token"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_missing_field(self):
        results = evaluate_assertions(
            [{"type": "json_path_exists", "path": "data.missing"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False

    def test_fail_non_json_body(self):
        results = evaluate_assertions(
            [{"type": "json_path_exists", "path": "code"}],
            "not json", 200, None
        )
        assert results[0]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# 8. json_path_regex
# ══════════════════════════════════════════════════════════════════════════════

class TestJsonPathRegex:
    body = js({"date": "2026-03-26", "id": "user_123"})

    def test_pass_date_pattern(self):
        results = evaluate_assertions(
            [{"type": "json_path_regex", "path": "date", "pattern": r"\d{4}-\d{2}-\d{2}"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_fail_pattern_no_match(self):
        results = evaluate_assertions(
            [{"type": "json_path_regex", "path": "date", "pattern": r"^\d{8}$"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False

    def test_pass_id_format(self):
        results = evaluate_assertions(
            [{"type": "json_path_regex", "path": "id", "pattern": r"^user_\d+$"}],
            self.body, 200, None
        )
        assert results[0]["passed"] is True

    def test_invalid_regex_does_not_crash(self):
        results = evaluate_assertions(
            [{"type": "json_path_regex", "path": "date", "pattern": "[bad("}],
            self.body, 200, None
        )
        assert results[0]["passed"] is False  # invalid regex → fail, not exception


# ══════════════════════════════════════════════════════════════════════════════
# 9. diff_score_lte
# ══════════════════════════════════════════════════════════════════════════════

class TestDiffScoreLte:
    def test_pass_zero_score(self):
        results = evaluate_assertions(
            [{"type": "diff_score_lte", "value": 0.1}],
            None, None, 0.0
        )
        assert results[0]["passed"] is True

    def test_pass_within_threshold(self):
        results = evaluate_assertions(
            [{"type": "diff_score_lte", "value": 0.1}],
            None, None, 0.05
        )
        assert results[0]["passed"] is True

    def test_fail_exceeds_threshold(self):
        results = evaluate_assertions(
            [{"type": "diff_score_lte", "value": 0.1}],
            None, None, 0.5
        )
        assert results[0]["passed"] is False

    def test_pass_string_threshold_from_frontend(self):
        # Frontend sends "0.1" as string
        results = evaluate_assertions(
            [{"type": "diff_score_lte", "value": "0.1"}],
            None, None, 0.05
        )
        assert results[0]["passed"] is True

    def test_none_score_treated_as_one(self):
        results = evaluate_assertions(
            [{"type": "diff_score_lte", "value": 0.5}],
            None, None, None  # no diff_score yet → treated as 1.0
        )
        assert results[0]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# 10. Multiple assertions
# ══════════════════════════════════════════════════════════════════════════════

class TestMultipleAssertions:
    def test_all_pass(self):
        body = js({"code": 0, "msg": "ok"})
        assertions = [
            {"type": "status_code_eq", "value": 200},
            {"type": "response_not_empty"},
            {"type": "json_path_eq", "path": "code", "value": 0},
        ]
        results = evaluate_assertions(assertions, body, 200, 0.0)
        assert all(r["passed"] for r in results)
        assert assertions_all_passed(results) is True

    def test_one_fails_all_passed_returns_false(self):
        body = js({"code": 1, "msg": "error"})
        assertions = [
            {"type": "status_code_eq", "value": 200},
            {"type": "json_path_eq", "path": "code", "value": 0},  # fails
        ]
        results = evaluate_assertions(assertions, body, 200, 0.0)
        assert assertions_all_passed(results) is False

    def test_empty_assertions_returns_empty(self):
        results = evaluate_assertions([], '{"a":1}', 200, 0.0)
        assert results == []

    def test_none_assertions_returns_empty(self):
        results = evaluate_assertions(None, '{"a":1}', 200, 0.0)
        assert results == []

    def test_assertions_all_passed_empty(self):
        assert assertions_all_passed([]) is True
        assert assertions_all_passed(None) is True

    def test_unknown_assertion_type(self):
        results = evaluate_assertions(
            [{"type": "nonexistent_type"}],
            '{}', 200, 0.0
        )
        assert results[0]["passed"] is False
        assert "未知断言类型" in results[0]["message"]
