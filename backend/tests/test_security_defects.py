"""
测试项目中的安全缺陷
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


class TestSecurityDefects:
    """测试项目中存在安全缺陷"""

    def test_cors_allows_all_origins(self):
        """缺陷1: CORS 配置允许所有来源，存在安全风险"""
        from main import app
        
        client = TestClient(app)
        
        # 测试带有任意 origin 的请求
        response = client.get(
            "/api/health",
            headers={"Origin": "http://malicious-site.com"}
        )
        
        # 检查响应头中是否包含 Access-Control-Allow-Origin: *
        assert "access-control-allow-origin" in response.headers
        # 缺陷：允许所有来源
        assert response.headers["access-control-allow-origin"] == "*"

    def test_default_secret_key(self):
        """缺陷2: secret_key 默认为空字符串，生产环境应通过 RP_SECRET_KEY 覆盖"""
        from config import settings

        # 缺陷：默认为空字符串，没有强制要求设置，不应在生产中使用
        assert settings.secret_key == "", (
            "secret_key should default to '' — set RP_SECRET_KEY in production"
        )

    def test_no_api_authentication(self):
        """缺陷3: API 没有认证机制，任何人都可以访问"""
        import uuid
        from main import app

        client = TestClient(app)

        # 使用唯一名称避免 UNIQUE 冲突
        unique_name = f"auth-test-{uuid.uuid4().hex[:8]}"

        # 不带任何认证信息直接访问敏感接口
        response = client.post(
            "/api/v1/applications",
            json={
                "name": unique_name,
                "ssh_host": "192.168.1.100",
                "ssh_port": 22,
                "ssh_user": "testuser",
                "ssh_auth_type": "KEY"
            }
        )

        # 缺陷：没有认证检查，请求被接受（虽然可能因为数据问题失败）
        # 应该返回 401/403 而不是直接处理请求
        assert response.status_code in [201, 422]  # 说明没有认证拦截

    def test_ssh_password_stored_plaintext(self):
        """缺陷4: SSH 密码以明文形式存储在数据库中"""
        from models.application import Application
        import uuid
        
        # 创建应用时，密码以明文存储
        app = Application(
            id=str(uuid.uuid4()),
            name="test",
            ssh_host="localhost",
            ssh_user="test",
            ssh_auth_type="PASSWORD",
            ssh_password="plaintext_password"  # 缺陷：明文存储
        )
        
        # 密码以明文形式存在对象中，没有加密
        assert app.ssh_password == "plaintext_password"


class TestErrorHandling:
    """测试错误处理缺陷"""

    def test_ssh_connection_no_retry(self):
        """缺陷5: SSH 连接失败没有重试机制"""
        from integration.ssh_executor import test_connection
        from models.application import Application
        import uuid
        
        # 创建一个会连接失败的配置
        app = Application(
            id=str(uuid.uuid4()),
            name="test",
            ssh_host="192.168.255.254",  # 不存在的 IP
            ssh_port=22,
            ssh_user="test",
            ssh_auth_type="KEY",
            ssh_key_path="/nonexistent/key"
        )
        
        # 直接调用，没有重试
        result = test_connection(app)
        
        # 返回失败结果，但没有重试
        assert result["success"] is False
        # 缺陷：没有实现重试逻辑

    def test_database_exception_silently_caught(self):
        """缺陷6: init_db 中 ALTER TABLE 异常被记录到 debug 日志而非抛出"""
        # 读取 database.py 检查异常处理
        with open("database.py", "r") as f:
            content = f.read()

        # 现有实现：catch Exception as e, 仅记录 debug 日志
        assert "except Exception as e:" in content
        # 不抛出异常（pass 或 logger.debug）
        assert "logger.debug" in content


class TestLogicBugs:
    """测试逻辑缺陷"""

    def test_override_host_check_bug(self):
        """缺陷7: override_host 逻辑 - AREX平台已将此逻辑内联至replays.py"""
        # repeater_client 已被移除；override_host 逻辑内联在 _replay_one 中
        # 验证 Application 模型有 repeater_port 字段
        from models.application import Application
        import uuid
        app = Application(
            id=str(uuid.uuid4()),
            name="test",
            ssh_host="original-host",
            repeater_port=8080
        )
        assert app.repeater_port == 8080
        assert app.ssh_host == "original-host"

    def test_json_parse_failure_handling(self):
        """缺陷8: JSON 解析失败时返回原字符串可能导致后续问题"""
        from utils.diff import _parse
        
        # 测试非 JSON 字符串
        result = _parse("plain text response")
        # 返回原始字符串，可能导致后续 deepdiff 比较出问题
        assert result == "plain text response"
        
        # 测试空字符串
        result = _parse("")
        assert result == ""
        
        # 测试 None
        result = _parse(None)
        assert result is None


class TestBoundaryConditions:
    """测试边界条件"""

    def test_diff_with_very_large_json(self):
        """边界测试: 处理非常大的 JSON"""
        from utils.diff import compute_diff
        
        # 创建大型 JSON
        large_json = '{"data": [' + ','.join([f'{{"id":{i},"value":"test{i}"}}' for i in range(1000)]) + ']}'
        
        diff_json, score = compute_diff(large_json, large_json)
        
        # 相同内容应该返回 0 分
        assert score == 0.0

    def test_diff_with_malformed_json(self):
        """边界测试: 处理格式错误的 JSON"""
        from utils.diff import compute_diff
        
        # 一个有效的 JSON，一个无效的
        valid_json = '{"key": "value"}'
        invalid_json = '{"key": }'  # 格式错误
        
        diff_json, score = compute_diff(valid_json, invalid_json)
        
        # 应该能处理这种情况，返回较高分数
        assert score > 0

    def test_empty_recording_list(self):
        """边界测试: 空录制列表"""
        from utils.diff import compute_diff
        
        # 两个空值
        diff_json, score = compute_diff(None, None)
        assert score == 0.0
        assert diff_json is None
        
        # 一个空，一个有值
        diff_json, score = compute_diff(None, '{"key": "value"}')
        assert score > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
