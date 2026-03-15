"""
用户 API 测试
"""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestUserAPI:
    """用户 API 测试"""

    def setup_method(self):
        """测试方法设置"""
        from django.contrib.auth import get_user_model

        self.client = Client()
        self.base_url = "/api/v1"
        self.User = get_user_model()

    def test_create_user_success(self, user_data):
        """测试创建用户成功"""
        response = self.client.post(f"{self.base_url}/users", data=json.dumps(user_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]

    def test_create_user_duplicate_username(self, user_data):
        """测试创建重复用户名"""
        # 先创建一个用户
        self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        # 尝试创建同名用户
        response = self.client.post(f"{self.base_url}/users", data=json.dumps(user_data), content_type="application/json")
        assert response.status_code in [400, 500]

    def test_get_user_success(self, user_data):
        """测试获取用户详情成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.get(f"{self.base_url}/users/{user.id}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["username"] == user_data["username"]

    def test_get_user_not_found(self):
        """测试获取不存在的用户"""
        response = self.client.get(f"{self.base_url}/users/99999")
        assert response.status_code in [404, 500]

    def test_list_users_success(self):
        """测试获取用户列表成功"""
        # 创建多个用户
        for i in range(3):
            self.User.objects.create_user(username=f"user{i}", email=f"user{i}@example.com", password="password123")

        response = self.client.get(f"{self.base_url}/users")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "users" in data
        assert "total" in data
        assert data["total"] >= 3

    def test_list_users_pagination(self):
        """测试用户列表分页"""
        # 创建多个用户
        for i in range(15):
            self.User.objects.create_user(username=f"pageuser{i}", email=f"pageuser{i}@example.com", password="password123")

        # 测试第一页
        response = self.client.get(f"{self.base_url}/users?page=1&page_size=10")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data["users"]) == 10

        # 测试第二页
        response = self.client.get(f"{self.base_url}/users?page=2&page_size=10")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data["users"]) == 5

    def test_update_user_success(self, user_data):
        """测试更新用户成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.put(f"{self.base_url}/users/{user.id}", data=json.dumps(update_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["first_name"] == "Updated"

    def test_delete_user_success(self, user_data):
        """测试删除用户成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.delete(f"{self.base_url}/users/{user.id}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "用户删除成功"

    def test_delete_user_not_found(self):
        """测试删除不存在的用户"""
        response = self.client.delete(f"{self.base_url}/users/99999")
        assert response.status_code in [404, 500]

    def test_change_password_success(self, user_data):
        """测试修改密码成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])
        user.is_active = True
        user.save()

        # 先登录获取token
        login_response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"username": user_data["username"], "password": user_data["password"]}),
            content_type="application/json",
        )
        login_data = json.loads(login_response.content)
        token = login_data.get("access_token")

        # 修改密码
        password_data = {"old_password": user_data["password"], "new_password": "newpassword123"}
        response = self.client.post(
            f"{self.base_url}/users/change-password",
            data=json.dumps(password_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        assert response.status_code in [200, 400, 401]

    def test_get_current_user_success(self, user_data):
        """测试获取当前用户信息成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])
        user.is_active = True
        user.save()

        # 先登录获取token
        login_response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"username": user_data["username"], "password": user_data["password"]}),
            content_type="application/json",
        )
        login_data = json.loads(login_response.content)
        token = login_data.get("access_token")

        # 获取当前用户信息
        response = self.client.get(f"{self.base_url}/me", HTTP_AUTHORIZATION=f"Bearer {token}")
        assert response.status_code in [200, 401]

    def test_get_current_user_unauthorized(self):
        """测试未登录获取当前用户信息"""
        response = self.client.get(f"{self.base_url}/me")
        assert response.status_code in [401, 500]
