"""
Unit tests for utils/desensitize.py — desensitize_body.
Run: cd backend && python -m pytest tests/test_desensitize.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import pytest
from utils.desensitize import desensitize_body


def js(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)

def parse(s: str) -> dict:
    return json.loads(s)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Basic pass-through (no rules or no body)
# ══════════════════════════════════════════════════════════════════════════════

class TestPassThrough:
    def test_none_body_returns_none(self):
        assert desensitize_body(None, [{"field": "pw", "action": "mask"}]) is None

    def test_empty_body_returns_empty(self):
        assert desensitize_body("", [{"field": "pw", "action": "mask"}]) == ""

    def test_no_rules_returns_body_unchanged(self):
        body = js({"password": "secret"})
        assert desensitize_body(body, []) == body
        assert desensitize_body(body, None) == body

    def test_non_json_body_returned_unchanged(self):
        body = "plain text response"
        result = desensitize_body(body, [{"field": "anything", "action": "mask"}])
        assert result == body


# ══════════════════════════════════════════════════════════════════════════════
# 2. action: mask
# ══════════════════════════════════════════════════════════════════════════════

class TestMask:
    def test_mask_top_level_field(self):
        body = js({"username": "alice", "password": "secret123"})
        result = parse(desensitize_body(body, [{"field": "password", "action": "mask"}]))
        assert result["password"] == "***"
        assert result["username"] == "alice"

    def test_mask_nested_field(self):
        body = js({"user": {"token": "abc123", "name": "bob"}})
        result = parse(desensitize_body(body, [{"field": "token", "action": "mask"}]))
        assert result["user"]["token"] == "***"
        assert result["user"]["name"] == "bob"

    def test_mask_field_in_list(self):
        body = js({"users": [{"id": 1, "token": "t1"}, {"id": 2, "token": "t2"}]})
        result = parse(desensitize_body(body, [{"field": "token", "action": "mask"}]))
        assert result["users"][0]["token"] == "***"
        assert result["users"][1]["token"] == "***"
        assert result["users"][0]["id"] == 1

    def test_mask_null_value(self):
        body = js({"password": None})
        result = parse(desensitize_body(body, [{"field": "password", "action": "mask"}]))
        assert result["password"] == "***"

    def test_mask_integer_value(self):
        body = js({"card_no": 1234567890})
        result = parse(desensitize_body(body, [{"field": "card_no", "action": "mask"}]))
        assert result["card_no"] == "***"


# ══════════════════════════════════════════════════════════════════════════════
# 3. action: remove
# ══════════════════════════════════════════════════════════════════════════════

class TestRemove:
    def test_remove_field(self):
        body = js({"name": "alice", "password": "secret"})
        result = parse(desensitize_body(body, [{"field": "password", "action": "remove"}]))
        assert "password" not in result
        assert result["name"] == "alice"

    def test_remove_nested_field(self):
        body = js({"data": {"id": 1, "ssn": "123-45-6789"}})
        result = parse(desensitize_body(body, [{"field": "ssn", "action": "remove"}]))
        assert "ssn" not in result["data"]
        assert result["data"]["id"] == 1

    def test_remove_field_in_list(self):
        body = js({"items": [{"name": "a", "secret": "x"}, {"name": "b", "secret": "y"}]})
        result = parse(desensitize_body(body, [{"field": "secret", "action": "remove"}]))
        for item in result["items"]:
            assert "secret" not in item

    def test_remove_missing_field_no_error(self):
        body = js({"name": "alice"})
        result = parse(desensitize_body(body, [{"field": "nonexistent", "action": "remove"}]))
        assert result == {"name": "alice"}


# ══════════════════════════════════════════════════════════════════════════════
# 4. action: partial
# ══════════════════════════════════════════════════════════════════════════════

class TestPartial:
    def test_phone_partial(self):
        body = js({"phone": "13812345678"})
        result = parse(desensitize_body(
            body,
            [{"field": "phone", "action": "partial", "keep_start": 3, "keep_end": 4}]
        ))
        phone = result["phone"]
        assert phone.startswith("138")
        assert phone.endswith("5678")
        assert "*" in phone
        # Length should match original
        assert len(phone) == len("13812345678")

    def test_short_string_all_masked(self):
        # String shorter than keep_start + keep_end → all stars
        body = js({"code": "abc"})
        result = parse(desensitize_body(
            body,
            [{"field": "code", "action": "partial", "keep_start": 3, "keep_end": 3}]
        ))
        assert result["code"] == "***"

    def test_exact_boundary(self):
        # "1234" with keep_start=2, keep_end=2 → len=4 <= 4 → "****"
        body = js({"v": "1234"})
        result = parse(desensitize_body(
            body,
            [{"field": "v", "action": "partial", "keep_start": 2, "keep_end": 2}]
        ))
        assert result["v"] == "****"

    def test_default_keep_params(self):
        # Default keep_start=3, keep_end=4
        body = js({"phone": "13812345678"})
        result = parse(desensitize_body(
            body,
            [{"field": "phone", "action": "partial"}]  # no keep params
        ))
        phone = result["phone"]
        assert phone.startswith("138")
        assert phone.endswith("5678")

    def test_integer_value_treated_as_string(self):
        body = js({"card": 1234567890123456})
        result = parse(desensitize_body(
            body,
            [{"field": "card", "action": "partial", "keep_start": 4, "keep_end": 4}]
        ))
        card = result["card"]
        assert card.startswith("1234")
        assert card.endswith("3456")


# ══════════════════════════════════════════════════════════════════════════════
# 5. action: hash
# ══════════════════════════════════════════════════════════════════════════════

class TestHash:
    def test_hash_format(self):
        body = js({"id_card": "110101199001011234"})
        result = parse(desensitize_body(body, [{"field": "id_card", "action": "hash"}]))
        hashed = result["id_card"]
        assert hashed.startswith("hash:")
        assert len(hashed) == len("hash:") + 8

    def test_hash_is_deterministic(self):
        body = js({"secret": "mysecret"})
        rules = [{"field": "secret", "action": "hash"}]
        r1 = parse(desensitize_body(body, rules))
        r2 = parse(desensitize_body(body, rules))
        assert r1["secret"] == r2["secret"]

    def test_different_values_produce_different_hashes(self):
        body1 = js({"secret": "value_a"})
        body2 = js({"secret": "value_b"})
        rules = [{"field": "secret", "action": "hash"}]
        r1 = parse(desensitize_body(body1, rules))
        r2 = parse(desensitize_body(body2, rules))
        assert r1["secret"] != r2["secret"]

    def test_hash_null_value(self):
        body = js({"secret": None})
        result = parse(desensitize_body(body, [{"field": "secret", "action": "hash"}]))
        assert result["secret"].startswith("hash:")


# ══════════════════════════════════════════════════════════════════════════════
# 6. Multiple rules
# ══════════════════════════════════════════════════════════════════════════════

class TestMultipleRules:
    def test_multiple_fields_different_actions(self):
        body = js({
            "name": "alice",
            "password": "secret",
            "phone": "13812345678",
            "token": "eyJhbGci...",
        })
        rules = [
            {"field": "password", "action": "remove"},
            {"field": "phone", "action": "partial", "keep_start": 3, "keep_end": 4},
            {"field": "token", "action": "mask"},
        ]
        result = parse(desensitize_body(body, rules))
        assert "password" not in result
        assert result["phone"].startswith("138")
        assert result["token"] == "***"
        assert result["name"] == "alice"

    def test_rule_without_field_key_skipped(self):
        body = js({"password": "secret"})
        rules = [{"action": "mask"}]  # no "field" key
        result = parse(desensitize_body(body, rules))
        # No rule matched → unchanged
        assert result["password"] == "secret"

    def test_deeply_nested_structure(self):
        body = js({
            "level1": {
                "level2": {
                    "password": "deep_secret",
                    "name": "nested",
                }
            }
        })
        result = parse(desensitize_body(
            body,
            [{"field": "password", "action": "mask"}]
        ))
        assert result["level1"]["level2"]["password"] == "***"
        assert result["level1"]["level2"]["name"] == "nested"


# ══════════════════════════════════════════════════════════════════════════════
# 7. Output is valid JSON
# ══════════════════════════════════════════════════════════════════════════════

class TestOutputIsJson:
    def test_result_is_valid_json(self):
        body = js({"a": 1, "password": "secret", "name": "中文名"})
        result = desensitize_body(body, [{"field": "password", "action": "mask"}])
        # Must not raise
        parsed = json.loads(result)
        assert parsed["name"] == "中文名"

    def test_unicode_preserved(self):
        body = js({"msg": "成功", "token": "abc"})
        result = desensitize_body(body, [{"field": "token", "action": "remove"}])
        parsed = json.loads(result)
        assert parsed["msg"] == "成功"
        assert "token" not in parsed
