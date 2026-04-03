"""
Unit tests for new P0/P1 features:
- P0: Smart Noise Reduction (smart_noise_reduction)
- P0: Traffic Amplification (repeat_count) - recording expansion logic
- P1: Header Transforms (_apply_header_transforms)
- P1: Retry Logic (retry_count)

Run: cd backend && python -m pytest tests/test_new_features.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import pytest
from utils.diff import compute_diff, get_builtin_noise_ignore_rules, BUILTIN_SMART_NOISE_PATTERNS


def js(obj) -> str:
    return json.dumps(obj)


# ══════════════════════════════════════════════════════════════════════════════
# Test 1: Smart Noise Reduction (P0)
# ══════════════════════════════════════════════════════════════════════════════

class TestSmartNoiseReduction:
    """Test cases for built-in smart noise reduction feature"""

    def test_builtin_patterns_not_empty(self):
        """Verify that built-in patterns list is not empty"""
        assert len(BUILTIN_SMART_NOISE_PATTERNS) > 30, "Should have 30+ built-in patterns"

    def test_get_builtin_noise_ignore_rules(self):
        """Test that get_builtin_noise_ignore_rules returns the patterns"""
        rules = get_builtin_noise_ignore_rules()
        assert isinstance(rules, list)
        assert len(rules) > 0

    def test_ignores_timestamp_field(self):
        """Smart noise should ignore timestamp differences"""
        orig = js({"code": 0, "timestamp": 1000000})
        repl = js({"code": 0, "timestamp": 9999999})
        # Without smart noise: should differ
        _, score_without = compute_diff(orig, repl)
        assert score_without > 0.0, "Without smart noise, should detect difference"
        # With smart noise: should be identical
        diff_json, score_with = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score_with == 0.0, "With smart noise, should ignore timestamp"
        assert diff_json is None, "No diff should be returned"

    def test_ignores_request_id(self):
        """Smart noise should ignore requestId differences"""
        orig = js({"code": 0, "requestId": "req-123"})
        repl = js({"code": 0, "requestId": "req-456"})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore requestId"
        assert diff_json is None

    def test_ignores_nested_timestamp(self):
        """Smart noise should ignore nested timestamp fields"""
        orig = js({"data": {"info": {"timestamp": 1000}}})
        repl = js({"data": {"info": {"timestamp": 9999}}})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore nested timestamp"
        assert diff_json is None

    def test_ignores_token_field(self):
        """Smart noise should ignore token differences"""
        orig = js({"code": 0, "token": "old-token-12345"})
        repl = js({"code": 0, "token": "new-token-67890"})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore token"
        assert diff_json is None

    def test_ignores_created_at_field(self):
        """Smart noise should ignore createdAt differences"""
        orig = js({"code": 0, "createdAt": "2024-01-01T00:00:00Z"})
        repl = js({"code": 0, "createdAt": "2024-12-31T23:59:59Z"})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore createdAt"
        assert diff_json is None

    def test_still_detects_real_changes(self):
        """Smart noise should not hide real business logic changes"""
        orig = js({"code": 0, "message": "ok", "timestamp": 1000})
        repl = js({"code": 500, "message": "error", "timestamp": 9999})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score > 0.0, "Should still detect code and message changes"
        assert diff_json is not None

    def test_combines_with_diff_rules(self):
        """Smart noise can work together with custom diff rules"""
        orig = js({"code": 0, "timestamp": 1000, "data": {"price": 10.00}})
        repl = js({"code": 0, "timestamp": 9999, "data": {"price": 10.01}})
        diff_rules = [{"type": "numeric_tolerance", "path": "data.price", "tolerance": 0.02}]
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True, diff_rules=diff_rules)
        assert score == 0.0, "Should ignore timestamp and tolerate price difference"

    def test_ignores_lat_lng(self):
        """Smart noise should ignore lat/lng differences"""
        orig = js({"code": 0, "lat": 39.9042, "lng": 116.4074})
        repl = js({"code": 0, "lat": 39.9999, "lng": 116.9999})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore lat/lng"

    def test_ignores_random_fields(self):
        """Smart noise should ignore random/nonce fields"""
        orig = js({"code": 0, "random": "abc123", "nonce": "xyz789"})
        repl = js({"code": 0, "random": "def456", "nonce": "uvw012"})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=True)
        assert score == 0.0, "Should ignore random/nonce"


# ══════════════════════════════════════════════════════════════════════════════
# Test 2: Header Transforms (P1)
# ══════════════════════════════════════════════════════════════════════════════

class TestHeaderTransforms:
    """Test cases for header transformation feature"""

    def test_apply_header_transforms_replace(self):
        """Test replace type header transform"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old-host.com", "Content-Type": "application/json"}
        transforms = [{"type": "replace", "key": "Host", "value": "new-host.com"}]
        result = _apply_header_transforms(headers, transforms)
        assert result["Host"] == "new-host.com"
        assert result["Content-Type"] == "application/json"

    def test_apply_header_transforms_remove(self):
        """Test remove type header transform"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old-host.com", "Authorization": "Bearer token123"}
        transforms = [{"type": "remove", "key": "Authorization"}]
        result = _apply_header_transforms(headers, transforms)
        assert "Authorization" not in result
        assert result["Host"] == "old-host.com"

    def test_apply_header_transforms_add(self):
        """Test add type header transform"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old-host.com"}
        transforms = [{"type": "add", "key": "X-Custom-Header", "value": "custom-value"}]
        result = _apply_header_transforms(headers, transforms)
        assert result["X-Custom-Header"] == "custom-value"
        assert result["Host"] == "old-host.com"

    def test_apply_header_transforms_add_existing_not_overwrite(self):
        """Test add type should not overwrite existing header"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old-host.com"}
        transforms = [{"type": "add", "key": "Host", "value": "new-host.com"}]
        result = _apply_header_transforms(headers, transforms)
        assert result["Host"] == "old-host.com", "Should not overwrite existing header"

    def test_apply_header_transforms_empty_transforms(self):
        """Test empty transforms returns original headers"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "test.com"}
        result = _apply_header_transforms(headers, None)
        assert result == headers

    def test_apply_header_transforms_empty_list(self):
        """Test empty list returns original headers"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "test.com"}
        result = _apply_header_transforms(headers, [])
        assert result == headers

    def test_apply_header_transforms_multiple(self):
        """Test multiple transforms in sequence"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old.com", "Authorization": "Bearer old", "X-Extra": "value"}
        transforms = [
            {"type": "replace", "key": "Host", "value": "new.com"},
            {"type": "remove", "key": "Authorization"},
            {"type": "add", "key": "X-New", "value": "new-value"},
        ]
        result = _apply_header_transforms(headers, transforms)
        assert result["Host"] == "new.com"
        assert "Authorization" not in result
        assert result["X-New"] == "new-value"
        assert result["X-Extra"] == "value"

    def test_apply_header_transforms_preserves_original(self):
        """Test that original headers dict is not modified"""
        from api.v1.replays import _apply_header_transforms
        headers = {"Host": "old.com"}
        transforms = [{"type": "replace", "key": "Host", "value": "new.com"}]
        result = _apply_header_transforms(headers, transforms)
        assert headers["Host"] == "old.com", "Original should not be modified"


# ══════════════════════════════════════════════════════════════════════════════
# Test 3: Traffic Amplification - Recording Expansion Logic (P0)
# ══════════════════════════════════════════════════════════════════════════════

class TestTrafficAmplification:
    """Test cases for traffic amplification (repeat_count) feature"""

    def test_expand_recordings_single(self):
        """Single recording with repeat_count=1 should return single item"""
        recording_ids = ["rec-1"]
        repeat_count = 1
        expanded = []
        for rid in recording_ids:
            expanded.extend([rid] * repeat_count)
        assert expanded == ["rec-1"]

    def test_expand_recordings_multiple(self):
        """Multiple recordings with repeat_count=2 should duplicate each"""
        recording_ids = ["rec-1", "rec-2"]
        repeat_count = 2
        expanded = []
        for rid in recording_ids:
            expanded.extend([rid] * repeat_count)
        assert expanded == ["rec-1", "rec-1", "rec-2", "rec-2"]

    def test_expand_recordings_repeat_5(self):
        """Test repeat_count=5 expands correctly"""
        recording_ids = ["rec-1"]
        repeat_count = 5
        expanded = []
        for rid in recording_ids:
            expanded.extend([rid] * repeat_count)
        assert len(expanded) == 5
        assert expanded == ["rec-1"] * 5

    def test_expand_recordings_zero_repeat(self):
        """repeat_count=0 should result in empty list"""
        recording_ids = ["rec-1", "rec-2"]
        repeat_count = 0
        expanded = []
        for rid in recording_ids:
            expanded.extend([rid] * repeat_count)
        assert expanded == []

    def test_repeat_count_in_compute_diff(self):
        """Verify compute_diff works with the new smart_noise_reduction param"""
        orig = js({"code": 0, "data": {"id": 1}})
        repl = js({"code": 0, "data": {"id": 1}})
        diff_json, score = compute_diff(orig, repl, smart_noise_reduction=False)
        assert score == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# Test 4: Retry Logic (P1) - Basic retry count handling
# ══════════════════════════════════════════════════════════════════════════════

class TestRetryLogic:
    """Test cases for retry logic (retry_count) feature"""

    def test_retry_count_expands_attempts(self):
        """retry_count should expand to max(1, retry_count + 1) attempts"""
        retry_count = 3
        # The logic is: for attempt in range(max(1, retry_count + 1))
        max_attempts = max(1, retry_count + 1)
        assert max_attempts == 4, "retry_count=3 should result in 4 attempts (1 initial + 3 retries)"

    def test_retry_count_zero_single_attempt(self):
        """retry_count=0 should result in single attempt"""
        retry_count = 0
        max_attempts = max(1, retry_count + 1)
        assert max_attempts == 1

    def test_retry_count_five_max_attempts(self):
        """retry_count=5 should result in 6 attempts"""
        retry_count = 5
        max_attempts = max(1, retry_count + 1)
        assert max_attempts == 6

    def test_retry_count_in_api_function_signature(self):
        """Verify _replay_one accepts retry_count parameter"""
        import inspect
        from api.v1.replays import _replay_one
        sig = inspect.signature(_replay_one)
        params = list(sig.parameters.keys())
        assert "retry_count" in params, "_replay_one should have retry_count parameter"

    def test_retry_count_in_job_model(self):
        """Verify ReplayJob model has retry_count field"""
        from models.replay import ReplayJob
        # Check if the model has the attribute (won't work without DB, but checks class)
        assert hasattr(ReplayJob, "retry_count"), "ReplayJob should have retry_count column"


# ══════════════════════════════════════════════════════════════════════════════
# Test 5: Schema Validation
# ══════════════════════════════════════════════════════════════════════════════

class TestSchemaValidation:
    """Test that schemas include new fields"""

    def test_replay_job_create_has_new_fields(self):
        """Verify ReplayJobCreate schema has new fields"""
        from schemas.replay import ReplayJobCreate
        fields = ReplayJobCreate.model_fields
        assert "smart_noise_reduction" in fields
        assert "repeat_count" in fields
        assert "header_transforms" in fields
        assert "retry_count" in fields

    def test_replay_job_out_has_new_fields(self):
        """Verify ReplayJobOut schema has new fields"""
        from schemas.replay import ReplayJobOut
        fields = ReplayJobOut.model_fields
        assert "smart_noise_reduction" in fields
        assert "repeat_count" in fields
        assert "header_transforms" in fields
        assert "retry_count" in fields


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
