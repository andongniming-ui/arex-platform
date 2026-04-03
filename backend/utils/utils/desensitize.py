"""
Data desensitization for recording storage.

desensitize_rules format (list of dicts):
  {"field": "password",  "action": "remove"}
  {"field": "token",     "action": "mask"}
  {"field": "phone",     "action": "partial", "keep_start": 3, "keep_end": 4}
  {"field": "id_card",   "action": "hash"}

Actions:
  remove  - delete the field entirely
  mask    - replace value with "***"
  partial - keep first keep_start and last keep_end characters, mask the middle
  hash    - replace with SHA256 hash prefix (first 8 chars)

The rules apply recursively to all occurrences of the field name in the JSON body.
"""
import json
import hashlib


def desensitize_body(body: str | None, rules: list[dict] | None) -> str | None:
    """
    Apply desensitization rules to a JSON body string.
    Returns the sanitized body string (re-serialized JSON).
    Non-JSON bodies are returned unchanged.
    """
    if not body or not rules:
        return body

    try:
        obj = json.loads(body)
    except Exception:
        return body

    rule_map = {r["field"]: r for r in rules if r.get("field")}
    obj = _apply_rules(obj, rule_map)
    return json.dumps(obj, ensure_ascii=False)


def _apply_rules(obj, rule_map: dict):
    """Recursively walk the object and apply rules to matching keys."""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key in rule_map:
                transformed = _transform_value(value, rule_map[key])
                if transformed is not _REMOVED:
                    result[key] = transformed
            else:
                result[key] = _apply_rules(value, rule_map)
        return result
    elif isinstance(obj, list):
        return [_apply_rules(item, rule_map) for item in obj]
    else:
        return obj


class _RemovedType:
    pass

_REMOVED = _RemovedType()


def _transform_value(value, rule: dict):
    action = rule.get("action", "mask")

    if action == "remove":
        return _REMOVED

    if action == "mask":
        return "***"

    if action == "partial":
        s = str(value) if value is not None else ""
        keep_start = int(rule.get("keep_start", 3))
        keep_end = int(rule.get("keep_end", 4))
        if len(s) <= keep_start + keep_end:
            return "*" * len(s)
        return s[:keep_start] + "*" * (len(s) - keep_start - keep_end) + s[-keep_end:]

    if action == "hash":
        s = str(value) if value is not None else ""
        digest = hashlib.sha256(s.encode()).hexdigest()[:8]
        return f"hash:{digest}"

    return "***"
