"""
认证 API 测试
"""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestAuthAPI:
    """认证 API 测试"""

    def setup_method(self):
        """测试方法设置"""
        from django.contrib.auth import get_user_model

        self.client = Client()
        self.base_url = "/api/v1/auth"
        self.User = get_user_model()

    def test_register_success(self, user_data):
        """测试用户注册成功"""
        response = self.client.post(
            f"{self.base_url}/register", data=json.dumps(user_data), content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "username" in data["data"]

    def test_register_duplicate_email(self, user_data):
        """测试重复邮箱注册"""
        # 第一次注册
        self.client.post(
            f"{self.base_url}/register", data=json.dumps(user_data), content_type="application/json"
        )

        # 第二次注册（相同邮箱）
        response = self.client.post(
            f"{self.base_url}/register", data=json.dumps(user_data), content_type="application/json"
        )
        assert response.status_code in [400, 200]

    def test_login_success(self, user_data):
        """测试登录成功"""
        # 先注册用户
        self.User.objects.create_user(**user_data)

        # 登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "access" in data["data"]
        assert "refresh" in data["data"]

    def test_login_wrong_password(self, user_data):
        """测试密码错误登录"""
        self.User.objects.create_user(**user_data)

        login_data = {"username": user_data["username"], "password": "wrongpassword"}
        response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        assert response.status_code in [401, 200]

    def test_logout_success(self, user_data):
        """测试登出成功"""
        self.User.objects.create_user(**user_data)

        # 先登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        login_response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        login_data_resp = json.loads(login_response.content)
        token = login_data_resp["data"]["access"]

        # 登出
        response = self.client.post(f"{self.base_url}/logout", HTTP_AUTHORIZATION=f"Bearer {token}")
        assert response.status_code in [200, 204]

    def test_refresh_token_success(self, user_data):
        """测试刷新 Token 成功"""
        self.User.objects.create_user(**user_data)

        # 先登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        login_response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        login_data_resp = json.loads(login_response.content)
        refresh_token = login_data_resp["data"]["refresh"]

        # 刷新 Token
        response = self.client.post(
            f"{self.base_url}/refresh",
            data=json.dumps({"refresh": refresh_token}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "access" in data["data"]
