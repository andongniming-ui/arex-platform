"""
Unit tests for utils/diff.py — compute_diff and Smart Diff Rules.
Run: cd backend && python -m pytest tests/test_diff.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import pytest
from utils.diff import compute_diff, _split_path, _path_to_deepdiff_regex, _transform_at_path_with_other


# ── Helpers ────────────────────────────────────────────────────────────────────

def js(obj) -> str:
    return json.dumps(obj)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Basic compute_diff (no rules)
# ══════════════════════════════════════════════════════════════════════════════

class TestBasicDiff:
    def test_identical_returns_none_and_zero(self):
        body = js({"code": 0, "data": {"id": 1}})
        diff_json, score = compute_diff(body, body)
        assert diff_json is None
        assert score == 0.0

    def test_both_none(self):
        diff_json, score = compute_diff(None, None)
        assert diff_json is None
        assert score == 0.0

    def test_one_none(self):
        # original exists, replayed is None — should differ
        diff_json, score = compute_diff(js({"a": 1}), None)
        assert score > 0.0

    def test_value_changed(self):
        orig = js({"code": 0, "msg": "ok"})
        repl = js({"code": 1, "msg": "ok"})
        diff_json, score = compute_diff(orig, repl)
        assert diff_json is not None
        assert score > 0.0

    def test_field_added(self):
        orig = js({"a": 1})
        repl = js({"a": 1, "b": 2})
        diff_json, score = compute_diff(orig, repl)
        assert diff_json is not None
        assert score > 0.0

    def test_non_json_strings_equal(self):
        diff_json, score = compute_diff("hello", "hello")
        assert diff_json is None
        assert score == 0.0

    def test_non_json_strings_differ(self):
        diff_json, score = compute_diff("hello", "world")
        assert diff_json is not None
        assert score > 0.0

    def test_score_capped_at_one(self):
        orig = js({"a": 1, "b": 2, "c": 3})
        repl = js({"x": 10, "y": 20, "z": 30})
        _, score = compute_diff(orig, repl)
        assert 0.0 <= score <= 1.0


# ══════════════════════════════════════════════════════════════════════════════
# 2. ignore_paths (old-style field exclusion)
# ══════════════════════════════════════════════════════════════════════════════

class TestIgnorePaths:
    def test_ignore_dynamic_field(self):
        orig = js({"code": 0, "timestamp": 1000})
        repl = js({"code": 0, "timestamp": 9999})
        # without ignore: should differ
        _, score_before = compute_diff(orig, repl)
        assert score_before > 0.0
        # with ignore: should be identical
        diff_json, score = compute_diff(orig, repl, ignore_paths=[r".*\['timestamp'\].*"])
        assert diff_json is None
        assert score == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 3. Smart Diff Rules — ignore
# ══════════════════════════════════════════════════════════════════════════════

class TestDiffRuleIgnore:
    def test_ignore_top_level_field(self):
        orig = js({"code": 0, "requestId": "abc"})
        repl = js({"code": 0, "requestId": "xyz"})
        rules = [{"type": "ignore", "path": "requestId"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_ignore_nested_field(self):
        orig = js({"data": {"id": 1, "ts": 1000}})
        repl = js({"data": {"id": 1, "ts": 9999}})
        rules = [{"type": "ignore", "path": "data.ts"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_ignore_does_not_hide_other_changes(self):
        orig = js({"code": 0, "ts": 1000})
        repl = js({"code": 1, "ts": 9999})
        rules = [{"type": "ignore", "path": "ts"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        # ts ignored, but code changed → still differs
        assert diff_json is not None
        assert score > 0.0

    def test_ignore_rule_with_no_path_skipped(self):
        orig = js({"a": 1})
        repl = js({"a": 2})
        rules = [{"type": "ignore", "path": ""}]  # empty path → skip
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert score > 0.0  # still detects the change


# ══════════════════════════════════════════════════════════════════════════════
# 4. Smart Diff Rules — numeric_tolerance
# ══════════════════════════════════════════════════════════════════════════════

class TestDiffRuleNumericTolerance:
    def test_within_tolerance_passes(self):
        orig = js({"price": 10.00})
        repl = js({"price": 10.005})
        rules = [{"type": "numeric_tolerance", "path": "price", "tolerance": 0.01}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_outside_tolerance_fails(self):
        orig = js({"price": 10.00})
        repl = js({"price": 10.02})
        rules = [{"type": "numeric_tolerance", "path": "price", "tolerance": 0.01}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is not None
        assert score > 0.0

    def test_exactly_at_tolerance_boundary_passes(self):
        orig = js({"v": 100})
        repl = js({"v": 101})
        rules = [{"type": "numeric_tolerance", "path": "v", "tolerance": 1}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_nested_numeric_tolerance(self):
        orig = js({"data": {"score": 95.0}})
        repl = js({"data": {"score": 95.3}})
        rules = [{"type": "numeric_tolerance", "path": "data.score", "tolerance": 0.5}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_non_numeric_field_unaffected(self):
        """tolerance rule on a string field should not crash, just leaves it unchanged"""
        orig = js({"name": "alice"})
        repl = js({"name": "bob"})
        rules = [{"type": "numeric_tolerance", "path": "name", "tolerance": 1.0}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert score > 0.0  # still detects the change


# ══════════════════════════════════════════════════════════════════════════════
# 5. Smart Diff Rules — regex_match
# ══════════════════════════════════════════════════════════════════════════════

class TestDiffRuleRegexMatch:
    def test_both_match_pattern_treated_as_equal(self):
        orig = js({"token": "Bearer eyJhbGci..."})
        repl = js({"token": "Bearer eyJuZXci..."})
        rules = [{"type": "regex_match", "path": "token", "pattern": r"^Bearer .+"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_only_one_matches_still_differs(self):
        orig = js({"status": "SUCCESS_123"})
        repl = js({"status": "FAILED"})
        rules = [{"type": "regex_match", "path": "status", "pattern": r"^SUCCESS"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        # orig matches → sentinel; repl doesn't → left as "FAILED"  → differ
        assert score > 0.0

    def test_invalid_regex_does_not_crash(self):
        orig = js({"x": "abc"})
        repl = js({"x": "abc"})
        rules = [{"type": "regex_match", "path": "x", "pattern": "[invalid("}]
        # Should not raise; comparison result may vary but must not error
        try:
            compute_diff(orig, repl, diff_rules=rules)
        except Exception as e:
            pytest.fail(f"compute_diff raised unexpectedly: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 6. Smart Diff Rules — type_only
# ══════════════════════════════════════════════════════════════════════════════

class TestDiffRuleTypeOnly:
    def test_same_type_different_value_passes(self):
        orig = js({"id": 100})
        repl = js({"id": 999})
        rules = [{"type": "type_only", "path": "id"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_different_type_fails(self):
        orig = js({"id": 100})
        repl = js({"id": "100"})
        rules = [{"type": "type_only", "path": "id"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        # int vs str → type names differ ("int" vs "str")
        assert score > 0.0

    def test_type_only_nested(self):
        orig = js({"data": {"count": 5}})
        repl = js({"data": {"count": 42}})
        rules = [{"type": "type_only", "path": "data.count"}]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 7. Multiple rules combined
# ══════════════════════════════════════════════════════════════════════════════

class TestMultipleRules:
    def test_ignore_plus_tolerance(self):
        orig = js({"ts": 1000, "price": 9.99, "code": 0})
        repl = js({"ts": 9999, "price": 10.00, "code": 0})
        rules = [
            {"type": "ignore", "path": "ts"},
            {"type": "numeric_tolerance", "path": "price", "tolerance": 0.02},
        ]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert diff_json is None
        assert score == 0.0

    def test_combined_still_detects_real_change(self):
        orig = js({"ts": 1000, "price": 9.99, "code": 0})
        repl = js({"ts": 9999, "price": 10.00, "code": 500})
        rules = [
            {"type": "ignore", "path": "ts"},
            {"type": "numeric_tolerance", "path": "price", "tolerance": 0.02},
        ]
        diff_json, score = compute_diff(orig, repl, diff_rules=rules)
        assert score > 0.0  # code changed


# ══════════════════════════════════════════════════════════════════════════════
# 8. Path parsing helpers
# ══════════════════════════════════════════════════════════════════════════════

class TestPathHelpers:
    def test_split_simple(self):
        assert _split_path("timestamp") == ["timestamp"]

    def test_split_nested(self):
        assert _split_path("data.price") == ["data", "price"]

    def test_split_with_wildcard(self):
        assert _split_path("items.*.id") == ["items", "*", "id"]

    def test_split_strips_dollar_prefix(self):
        assert _split_path("$.data.id") == ["data", "id"]

    def test_regex_single_key(self):
        regex = _path_to_deepdiff_regex(["timestamp"])
        import re
        assert re.search(regex, "root['timestamp']")
        assert not re.search(regex, "root['timestamp']['sub']")

    def test_regex_nested_keys(self):
        regex = _path_to_deepdiff_regex(["data", "price"])
        import re
        assert re.search(regex, "root['data']['price']")
        assert not re.search(regex, "root['data']['price']['sub']")

    def test_regex_wildcard(self):
        regex = _path_to_deepdiff_regex(["items", "*", "id"])
        import re
        assert re.search(regex, "root['items'][0]['id']")
        assert re.search(regex, "root['items'][99]['id']")
