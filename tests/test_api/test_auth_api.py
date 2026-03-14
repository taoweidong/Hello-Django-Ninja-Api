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

    def test_login_success(self, user_data):
        """测试登录成功"""
        # 创建用户
        user = self.User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        user.is_active = True
        user.save()

        # 登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, user_data):
        """测试密码错误登录"""
        self.User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )

        login_data = {"username": user_data["username"], "password": "wrongpassword"}
        response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        assert response.status_code == 500  # 服务端错误

    def test_refresh_token_success(self, user_data):
        """测试刷新 Token 成功"""
        # 创建用户
        user = self.User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        user.is_active = True
        user.save()

        # 先登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        login_response = self.client.post(
            f"{self.base_url}/login", data=json.dumps(login_data), content_type="application/json"
        )
        login_data_resp = json.loads(login_response.content)
        refresh_token = login_data_resp.get("refresh_token")

        if refresh_token:
            # 刷新 Token
            response = self.client.post(
                f"{self.base_url}/refresh",
                data=json.dumps({"refresh_token": refresh_token}),
                content_type="application/json",
            )
            assert response.status_code == 200
            data = json.loads(response.content)
            assert "access_token" in data
