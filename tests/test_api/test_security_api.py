"""
安全 API 测试
"""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestSecurityAPI:
    """安全 API 测试"""

    def setup_method(self):
        """测试方法设置"""
        self.client = Client()
        self.base_url = "/api/v1"

    # ========== IP黑名单测试 ==========

    def test_add_to_blacklist_success(self):
        """测试添加IP到黑名单成功"""
        blacklist_data = {"ip_address": "192.168.1.100", "reason": "恶意请求", "expire_days": 7}
        response = self.client.post(f"{self.base_url}/security/blacklist", data=json.dumps(blacklist_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["ip_address"] == "192.168.1.100"

    def test_list_blacklist_success(self):
        """测试获取黑名单列表成功"""
        # 先添加一个IP到黑名单
        blacklist_data = {"ip_address": "192.168.1.101", "reason": "测试黑名单"}
        self.client.post(f"{self.base_url}/security/blacklist", data=json.dumps(blacklist_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/security/blacklist")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_remove_from_blacklist_success(self):
        """测试从黑名单移除IP成功"""
        # 先添加一个IP到黑名单
        blacklist_data = {"ip_address": "192.168.1.102", "reason": "待移除"}
        self.client.post(f"{self.base_url}/security/blacklist", data=json.dumps(blacklist_data), content_type="application/json")

        response = self.client.delete(f"{self.base_url}/security/blacklist/192.168.1.102")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "IP已从黑名单移除"

    def test_remove_from_blacklist_not_found(self):
        """测试移除不在黑名单中的IP"""
        response = self.client.delete(f"{self.base_url}/security/blacklist/192.168.1.199")
        assert response.status_code == 500

    # ========== IP白名单测试 ==========

    def test_add_to_whitelist_success(self):
        """测试添加IP到白名单成功"""
        whitelist_data = {"ip_address": "192.168.2.100", "reason": "可信IP", "expire_days": 30}
        response = self.client.post(f"{self.base_url}/security/whitelist", data=json.dumps(whitelist_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["ip_address"] == "192.168.2.100"

    def test_list_whitelist_success(self):
        """测试获取白名单列表成功"""
        # 先添加一个IP到白名单
        whitelist_data = {"ip_address": "192.168.2.101", "reason": "测试白名单"}
        self.client.post(f"{self.base_url}/security/whitelist", data=json.dumps(whitelist_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/security/whitelist")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_remove_from_whitelist_success(self):
        """测试从白名单移除IP成功"""
        # 先添加一个IP到白名单
        whitelist_data = {"ip_address": "192.168.2.102", "reason": "待移除"}
        self.client.post(f"{self.base_url}/security/whitelist", data=json.dumps(whitelist_data), content_type="application/json")

        response = self.client.delete(f"{self.base_url}/security/whitelist/192.168.2.102")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "IP已从白名单移除"

    def test_remove_from_whitelist_not_found(self):
        """测试移除不在白名单中的IP"""
        response = self.client.delete(f"{self.base_url}/security/whitelist/192.168.2.199")
        assert response.status_code == 500

    # ========== 限流规则测试 ==========

    def test_create_rate_limit_rule_success(self):
        """测试创建限流规则成功"""
        rule_data = {"name": "测试限流规则", "path_pattern": "/api/v1/test/*", "limit": 100, "period": 60, "is_active": True}
        response = self.client.post(f"{self.base_url}/security/rate-limit", data=json.dumps(rule_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "测试限流规则"

    def test_list_rate_limit_rules_success(self):
        """测试获取限流规则列表成功"""
        # 先创建一个限流规则
        rule_data = {"name": "列表测试规则", "path_pattern": "/api/v1/list/*", "limit": 50, "period": 60}
        self.client.post(f"{self.base_url}/security/rate-limit", data=json.dumps(rule_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/security/rate-limit")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_toggle_rate_limit_rule_success(self):
        """测试切换限流规则状态成功"""
        # 先创建一个限流规则
        rule_data = {"name": "切换测试规则", "path_pattern": "/api/v1/toggle/*", "limit": 50, "period": 60}
        create_response = self.client.post(f"{self.base_url}/security/rate-limit", data=json.dumps(rule_data), content_type="application/json")
        rule = json.loads(create_response.content)

        response = self.client.put(f"{self.base_url}/security/rate-limit/{rule['rule_id']}/toggle")
        assert response.status_code == 200

    def test_delete_rate_limit_rule_success(self):
        """测试删除限流规则成功"""
        # 先创建一个限流规则
        rule_data = {"name": "待删除规则", "path_pattern": "/api/v1/delete/*", "limit": 50, "period": 60}
        create_response = self.client.post(f"{self.base_url}/security/rate-limit", data=json.dumps(rule_data), content_type="application/json")
        rule = json.loads(create_response.content)

        response = self.client.delete(f"{self.base_url}/security/rate-limit/{rule['rule_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "限流规则删除成功"

    def test_delete_rate_limit_rule_not_found(self):
        """测试删除不存在的限流规则"""
        response = self.client.delete(f"{self.base_url}/security/rate-limit/99999")
        assert response.status_code == 500

    # ========== 安全状态测试 ==========

    def test_get_security_status_success(self):
        """测试获取安全状态成功"""
        response = self.client.get(f"{self.base_url}/security/status")
        assert response.status_code == 200
        data = json.loads(response.content)
        # 验证返回的状态信息结构
        assert isinstance(data, dict)
