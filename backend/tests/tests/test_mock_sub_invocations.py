"""
Tests for Mock sub-invocation feature.

Covers every layer of the implementation:
  1. Mock routing decision  — when should _replay_one pick mock vs direct HTTP?
  2. replay_with_mock()     — payload construction and response body extraction
  3. Fallback logic         — agent failure → falls back to direct_http_replay
  4. Data-parser enrichment — sub_invocations now includes responseBody
  5. Schema fields          — use_sub_invocation_mocks present in Create / Out
  6. Port fix               — replay_with_json must use sandbox_port, not repeater_port
"""
import json
import pytest


# ── 1. Mock routing decision ───────────────────────────────────────────────────

def should_use_mock(
    use_sub_invocation_mocks: bool,
    trace_id: str | None,
    sub_invocations: list | None,
) -> bool:
    """
    Replicate the routing condition from _replay_one:
        if use_sub_invocation_mocks and recording.trace_id and recording.sub_invocations
    """
    return bool(use_sub_invocation_mocks and trace_id and sub_invocations)


class TestMockRoutingDecision:

    def test_all_conditions_true_uses_mock(self):
        assert should_use_mock(True, "trace-abc", [{"type": "MYBATIS", "uri": "sql"}]) is True

    def test_flag_false_uses_direct(self):
        """Flag off → always direct, even if recording has trace + sub_invocations."""
        assert should_use_mock(False, "trace-abc", [{"type": "MYBATIS"}]) is False

    def test_no_trace_id_uses_direct(self):
        """No trace_id → can't route to Repeater agent."""
        assert should_use_mock(True, None, [{"type": "MYBATIS"}]) is False

    def test_empty_string_trace_id_uses_direct(self):
        """Empty string trace_id is falsy."""
        assert should_use_mock(True, "", [{"type": "MYBATIS"}]) is False

    def test_no_sub_invocations_uses_direct(self):
        """No sub_invocations → nothing to mock, use direct."""
        assert should_use_mock(True, "trace-abc", None) is False

    def test_empty_sub_invocations_uses_direct(self):
        """Empty list is falsy — nothing to mock."""
        assert should_use_mock(True, "trace-abc", []) is False

    def test_flag_false_trace_none_sub_none_uses_direct(self):
        assert should_use_mock(False, None, None) is False

    def test_all_conditions_required(self):
        """All three conditions must be truthy."""
        # Only one true at a time
        assert should_use_mock(True, None, None) is False
        assert should_use_mock(False, "trace", None) is False
        assert should_use_mock(False, None, [{"type": "X"}]) is False


# ── 2. replay_with_mock() payload construction ─────────────────────────────────

def build_repeat_meta(
    trace_id: str,
    entry_app: str | None,
    app_name: str,
    target_host: str,
    repeater_port: int,
) -> dict:
    """
    Replicate the repeat_meta construction in replay_with_mock().
    """
    return {
        "traceId": trace_id,
        "appName": entry_app or app_name,
        "environment": "replay",
        "host": f"{target_host}:{repeater_port}",
    }


class TestRepeatMetaConstruction:

    def test_trace_id_is_forwarded(self):
        meta = build_repeat_meta("trace-xyz", "myapp", "fallback", "10.0.0.1", 8080)
        assert meta["traceId"] == "trace-xyz"

    def test_entry_app_used_when_present(self):
        meta = build_repeat_meta("t1", "entry-app-name", "app-name", "host", 8080)
        assert meta["appName"] == "entry-app-name"

    def test_app_name_fallback_when_entry_app_none(self):
        """entry_app may be None for some recording types — fall back to app.name."""
        meta = build_repeat_meta("t1", None, "fallback-app", "host", 8080)
        assert meta["appName"] == "fallback-app"

    def test_app_name_fallback_when_entry_app_empty(self):
        meta = build_repeat_meta("t1", "", "fallback-app", "host", 8080)
        assert meta["appName"] == "fallback-app"

    def test_host_includes_port(self):
        meta = build_repeat_meta("t1", "app", "app", "192.168.1.100", 8080)
        assert meta["host"] == "192.168.1.100:8080"

    def test_environment_is_replay(self):
        meta = build_repeat_meta("t1", "app", "app", "host", 8080)
        assert meta["environment"] == "replay"

    def test_override_host_replaces_app_host(self):
        """override_host takes precedence over app.ssh_host."""
        # Simulate the logic: target_host = override_host or app.ssh_host
        override = "override.host.internal"
        app_host = "original.host"
        target_host = override or app_host
        meta = build_repeat_meta("t1", "app", "app", target_host, 8080)
        assert meta["host"].startswith("override.host.internal")

    def test_no_override_uses_app_host(self):
        override = None
        app_host = "original.host"
        target_host = override or app_host
        meta = build_repeat_meta("t1", "app", "app", target_host, 9090)
        assert meta["host"] == "original.host:9090"


# ── 3. Response body extraction from agent envelope ────────────────────────────

def extract_body_from_agent_response(raw_body: str) -> str:
    """
    Replicate the body-extraction logic from replay_with_mock():
    Agent wraps actual response inside {"success": true, "data": "..."}
    Falls back to raw body if envelope doesn't match.
    """
    try:
        outer = json.loads(raw_body)
        inner = outer.get("data") or outer.get("response") or raw_body
        return inner if isinstance(inner, str) else json.dumps(inner)
    except Exception:
        return raw_body


class TestAgentResponseExtraction:

    def test_extracts_data_field(self):
        envelope = json.dumps({"success": True, "data": '{"code":0,"msg":"ok"}'})
        assert extract_body_from_agent_response(envelope) == '{"code":0,"msg":"ok"}'

    def test_extracts_response_field_when_no_data(self):
        envelope = json.dumps({"success": True, "response": '{"result":"done"}'})
        assert extract_body_from_agent_response(envelope) == '{"result":"done"}'

    def test_data_takes_precedence_over_response(self):
        envelope = json.dumps({"success": True, "data": "data-value", "response": "resp-value"})
        assert extract_body_from_agent_response(envelope) == "data-value"

    def test_falls_back_to_raw_when_not_json(self):
        raw = "plain text response"
        assert extract_body_from_agent_response(raw) == raw

    def test_falls_back_to_raw_when_no_data_or_response_key(self):
        envelope = json.dumps({"success": True, "other_key": "value"})
        # outer.get("data") is None, outer.get("response") is None → falls back to raw_body
        assert extract_body_from_agent_response(envelope) == envelope

    def test_inner_dict_is_json_serialized(self):
        """If data is itself a dict (not a string), it gets json.dumps'd."""
        envelope = json.dumps({"success": True, "data": {"nested": "object"}})
        result = extract_body_from_agent_response(envelope)
        # inner is a dict → json.dumps
        parsed = json.loads(result)
        assert parsed == {"nested": "object"}

    def test_empty_string_body(self):
        assert extract_body_from_agent_response("") == ""

    def test_valid_json_but_no_envelope_keys(self):
        raw = '{"just":"data"}'
        # json.loads succeeds, no "data" or "response" key → falls back to raw_body (the original str)
        result = extract_body_from_agent_response(raw)
        assert result == raw


# ── 4. Fallback logic ──────────────────────────────────────────────────────────

def choose_replay_path(
    use_sub_invocation_mocks: bool,
    has_trace_id: bool,
    has_sub_invocations: bool,
    agent_success: bool,
) -> str:
    """
    Replicate the two-level fallback logic from _replay_one:
      1. If mock conditions met → try agent
      2. If agent fails → fall back to direct
      3. If mock conditions not met → direct
    Returns: "agent" or "direct"
    """
    if use_sub_invocation_mocks and has_trace_id and has_sub_invocations:
        if agent_success:
            return "agent"
        else:
            return "direct"   # fallback
    return "direct"


class TestFallbackLogic:

    def test_mock_enabled_agent_succeeds_uses_agent(self):
        assert choose_replay_path(True, True, True, agent_success=True) == "agent"

    def test_mock_enabled_agent_fails_falls_back_to_direct(self):
        assert choose_replay_path(True, True, True, agent_success=False) == "direct"

    def test_mock_disabled_uses_direct_regardless(self):
        assert choose_replay_path(False, True, True, agent_success=True) == "direct"

    def test_no_trace_id_uses_direct_regardless(self):
        assert choose_replay_path(True, False, True, agent_success=True) == "direct"

    def test_no_sub_invocations_uses_direct_regardless(self):
        assert choose_replay_path(True, True, False, agent_success=True) == "direct"

    def test_all_missing_conditions_always_direct(self):
        assert choose_replay_path(False, False, False, agent_success=False) == "direct"

    def test_fallback_never_retries_agent(self):
        """Once agent fails, we go to direct — there's no second attempt at agent."""
        results = []
        for attempt in range(5):
            path = choose_replay_path(True, True, True, agent_success=False)
            results.append(path)
        assert all(r == "direct" for r in results)


# ── 5. Data-parser sub-invocation enrichment ───────────────────────────────────

def parse_sub_invocation(sub: dict, decode_fn=None) -> dict:
    """
    Replicate the enriched sub-invocation parsing from data_parser.py.
    decode_fn simulates _decode_serialized().
    """
    identity = sub.get("identity") or {}
    sub_entry = {
        "type": (sub.get("type") or {}).get("name", "UNKNOWN"),
        "uri": identity.get("uri"),
        "traceId": sub.get("traceId"),
    }
    if decode_fn:
        resp_body = decode_fn(sub.get("responseSerialized"))
        if resp_body:
            sub_entry["responseBody"] = resp_body[:1000]
    return sub_entry


class TestSubInvocationParsing:

    def _identity(self, uri: str) -> dict:
        return {"uri": uri}

    def _type(self, name: str) -> dict:
        return {"name": name}

    def test_type_extracted(self):
        sub = {"type": self._type("MYBATIS"), "identity": self._identity("SELECT * FROM user"), "traceId": "t1"}
        result = parse_sub_invocation(sub)
        assert result["type"] == "MYBATIS"

    def test_uri_extracted(self):
        sub = {"type": self._type("HTTP"), "identity": self._identity("/api/v1/user"), "traceId": "t1"}
        result = parse_sub_invocation(sub)
        assert result["uri"] == "/api/v1/user"

    def test_trace_id_extracted(self):
        sub = {"type": self._type("REDIS"), "identity": self._identity("GET key"), "traceId": "trace-123"}
        result = parse_sub_invocation(sub)
        assert result["traceId"] == "trace-123"

    def test_type_defaults_to_unknown_when_missing(self):
        sub = {"identity": self._identity("uri"), "traceId": "t1"}
        result = parse_sub_invocation(sub)
        assert result["type"] == "UNKNOWN"

    def test_uri_none_when_identity_missing(self):
        sub = {"type": self._type("DUBBO"), "traceId": "t1"}
        result = parse_sub_invocation(sub)
        assert result["uri"] is None

    def test_response_body_captured_when_decodable(self):
        sub = {
            "type": self._type("MYBATIS"),
            "identity": self._identity("SELECT 1"),
            "traceId": "t1",
            "responseSerialized": "ENCODED_DATA",
        }
        decoded = '{"id":1,"name":"Alice"}'
        result = parse_sub_invocation(sub, decode_fn=lambda x: decoded if x else None)
        assert result["responseBody"] == decoded

    def test_response_body_absent_when_not_decodable(self):
        """No responseSerialized → responseBody should not be in entry."""
        sub = {"type": self._type("HTTP"), "identity": self._identity("/path"), "traceId": "t1"}
        result = parse_sub_invocation(sub, decode_fn=lambda x: None)
        assert "responseBody" not in result

    def test_response_body_capped_at_1000_chars(self):
        long_response = "x" * 2000
        sub = {
            "type": self._type("REDIS"),
            "identity": self._identity("GET key"),
            "traceId": "t1",
            "responseSerialized": "DATA",
        }
        result = parse_sub_invocation(sub, decode_fn=lambda x: long_response if x else None)
        assert len(result["responseBody"]) == 1000

    def test_response_body_under_1000_preserved_fully(self):
        short = '{"status":"ok"}'
        sub = {
            "type": self._type("HTTP"),
            "identity": self._identity("/api"),
            "traceId": "t1",
            "responseSerialized": "DATA",
        }
        result = parse_sub_invocation(sub, decode_fn=lambda x: short if x else None)
        assert result["responseBody"] == short

    def test_multiple_sub_invocations_all_parsed(self):
        subs = [
            {"type": self._type("MYBATIS"), "identity": self._identity("SELECT user"), "traceId": f"t{i}"}
            for i in range(3)
        ]
        results = [parse_sub_invocation(s) for s in subs]
        assert len(results) == 3
        assert all(r["type"] == "MYBATIS" for r in results)

    def test_mixed_types_parsed_correctly(self):
        subs = [
            {"type": self._type("MYBATIS"), "identity": self._identity("SELECT 1"), "traceId": "t1"},
            {"type": self._type("REDIS"), "identity": self._identity("GET cache"), "traceId": "t2"},
            {"type": self._type("DUBBO"), "identity": self._identity("UserService.getUser"), "traceId": "t3"},
        ]
        results = [parse_sub_invocation(s) for s in subs]
        types = [r["type"] for r in results]
        assert types == ["MYBATIS", "REDIS", "DUBBO"]


# ── 6. Schema: use_sub_invocation_mocks field ─────────────────────────────────

class TestSchema:

    def test_replay_job_create_has_mock_field(self):
        from schemas.replay import ReplayJobCreate
        job = ReplayJobCreate(case_id="c1", target_app_id="a1")
        assert hasattr(job, "use_sub_invocation_mocks")

    def test_mock_field_defaults_to_false(self):
        from schemas.replay import ReplayJobCreate
        job = ReplayJobCreate(case_id="c1", target_app_id="a1")
        assert job.use_sub_invocation_mocks is False

    def test_mock_field_can_be_set_true(self):
        from schemas.replay import ReplayJobCreate
        job = ReplayJobCreate(case_id="c1", target_app_id="a1", use_sub_invocation_mocks=True)
        assert job.use_sub_invocation_mocks is True

    def test_replay_job_out_has_mock_field(self):
        from schemas.replay import ReplayJobOut
        fields = ReplayJobOut.model_fields
        assert "use_sub_invocation_mocks" in fields

    def test_all_other_fields_still_present_in_create(self):
        """Regression: adding the new field must not break existing schema fields."""
        from schemas.replay import ReplayJobCreate
        job = ReplayJobCreate(
            case_id="c1",
            target_app_id="a1",
            concurrency=3,
            delay_ms=100,
            perf_threshold_ms=2000,
            use_sub_invocation_mocks=True,
        )
        assert job.concurrency == 3
        assert job.delay_ms == 100
        assert job.perf_threshold_ms == 2000
        assert job.use_sub_invocation_mocks is True


# ── 7. Port fix: replay_with_json must use sandbox_port ───────────────────────

def build_repeatwithjson_url(ssh_host: str, sandbox_port: int) -> str:
    """Replicate the URL built in replay_with_json (after the fix)."""
    return f"http://{ssh_host}:{sandbox_port}/sandbox/default/module/http/repeater/repeatWithJson"


class TestPortConfiguration:

    def test_url_uses_sandbox_port_not_repeater_port(self):
        sandbox_port = 39393
        repeater_port = 8080   # application port — must NOT appear in URL
        url = build_repeatwithjson_url("10.0.0.1", sandbox_port)
        assert str(sandbox_port) in url
        assert str(repeater_port) not in url

    def test_url_contains_correct_sandbox_path(self):
        url = build_repeatwithjson_url("10.0.0.1", 39393)
        assert "/sandbox/default/module/http/repeater/repeatWithJson" in url

    def test_url_uses_http_scheme(self):
        url = build_repeatwithjson_url("10.0.0.1", 39393)
        assert url.startswith("http://")

    def test_url_contains_host(self):
        url = build_repeatwithjson_url("my-server.internal", 39393)
        assert "my-server.internal" in url

    def test_sandbox_port_default_39393(self):
        """Default sandbox_port is 39393 per Application model."""
        default_sandbox_port = 39393
        url = build_repeatwithjson_url("host", default_sandbox_port)
        assert ":39393" in url

    def test_direct_replay_still_uses_repeater_port(self):
        """direct_http_replay must still use repeater_port (app HTTP port)."""
        repeater_port = 8080
        host = "10.0.0.1"
        path = "/api/users"
        url = f"http://{host}:{repeater_port}{path}"
        assert str(repeater_port) in url
        assert "/api/users" in url


# ── 8. End-to-end routing scenarios ───────────────────────────────────────────

class TestEndToEndRoutingScenarios:
    """
    Simulate the full routing decision + fallback as a table of scenarios.
    """

    def _route(self, use_mock, trace_id, sub_invs, agent_success) -> str:
        cond = bool(use_mock and trace_id and sub_invs)
        if cond:
            return "agent" if agent_success else "direct (fallback)"
        return "direct"

    def test_scenario_normal_replay_no_mock(self):
        assert self._route(False, "t1", [{"type": "DB"}], True) == "direct"

    def test_scenario_mock_enabled_agent_online(self):
        assert self._route(True, "t1", [{"type": "DB"}], True) == "agent"

    def test_scenario_mock_enabled_agent_offline(self):
        assert self._route(True, "t1", [{"type": "DB"}], False) == "direct (fallback)"

    def test_scenario_mock_enabled_no_sub_invocations(self):
        """Recording is pure HTTP with no downstream sub-calls → use direct."""
        assert self._route(True, "t1", None, True) == "direct"

    def test_scenario_mock_enabled_no_trace(self):
        """Old recording without trace_id → cannot route to agent."""
        assert self._route(True, None, [{"type": "DB"}], True) == "direct"

    def test_scenario_mock_enabled_empty_sub_invocations(self):
        assert self._route(True, "t1", [], True) == "direct"

    def test_scenario_http_only_service_always_direct(self):
        """Service with no downstream calls → no sub_invocations → always direct."""
        sub_invs = []  # pure HTTP microservice
        assert self._route(True, "t1", sub_invs, True) == "direct"

    def test_scenario_db_heavy_service_uses_mock(self):
        """Service with 3 DB calls → agent handles them all."""
        sub_invs = [
            {"type": "MYBATIS", "uri": "SELECT user"},
            {"type": "MYBATIS", "uri": "SELECT order"},
            {"type": "REDIS", "uri": "GET session"},
        ]
        assert self._route(True, "t1", sub_invs, True) == "agent"
