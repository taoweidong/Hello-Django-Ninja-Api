"""
RBAC API 测试
"""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestRBACAPI:
    """RBAC API 测试"""

    def setup_method(self):
        """测试方法设置"""
        from django.contrib.auth import get_user_model

        self.client = Client()
        self.base_url = "/api/v1/rbac"
        self.User = get_user_model()

    def test_create_role_success(self, role_data):
        """测试创建角色成功"""
        response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == role_data["name"]
        assert data["code"] == role_data["code"]

    def test_get_role_success(self, role_data):
        """测试获取角色详情成功"""
        # 先创建角色
        create_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(create_response.content)

        response = self.client.get(f"{self.base_url}/roles/{role['role_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == role_data["name"]

    def test_get_role_not_found(self):
        """测试获取不存在的角色"""
        response = self.client.get(f"{self.base_url}/roles/99999")
        assert response.status_code in [404, 500]

    def test_list_roles_success(self, role_data):
        """测试获取角色列表成功"""
        # 创建多个角色
        for i in range(3):
            role = role_data.copy()
            role["name"] = f"角色{i}"
            role["code"] = f"role_{i}"
            self.client.post(f"{self.base_url}/roles", data=json.dumps(role), content_type="application/json")

        response = self.client.get(f"{self.base_url}/roles")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "roles" in data
        assert "total" in data
        assert data["total"] >= 3

    def test_list_roles_filter_active(self, role_data):
        """测试按激活状态过滤角色"""
        # 创建角色
        role = role_data.copy()
        role["name"] = "激活角色"
        role["code"] = "active_role"
        self.client.post(f"{self.base_url}/roles", data=json.dumps(role), content_type="application/json")

        response = self.client.get(f"{self.base_url}/roles?is_active=true")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "roles" in data

    def test_update_role_success(self, role_data):
        """测试更新角色成功"""
        # 先创建角色
        create_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(create_response.content)

        update_data = {"name": "更新后的角色", "description": "更新后的描述"}
        response = self.client.put(f"{self.base_url}/roles/{role['role_id']}", data=json.dumps(update_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "更新后的角色"

    def test_delete_role_success(self, role_data):
        """测试删除角色成功"""
        # 先创建角色
        role = role_data.copy()
        role["name"] = "待删除角色"
        role["code"] = "delete_role"
        create_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role), content_type="application/json")
        role_data_resp = json.loads(create_response.content)

        response = self.client.delete(f"{self.base_url}/roles/{role_data_resp['role_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "角色删除成功"

    def test_list_permissions_success(self):
        """测试获取权限列表成功"""
        response = self.client.get(f"{self.base_url}/permissions")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "permissions" in data
        assert "total" in data

    def test_init_permissions_success(self):
        """测试初始化系统权限"""
        response = self.client.post(f"{self.base_url}/permissions/init")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "系统权限初始化成功"

    def test_assign_role_to_user_success(self, user_data, role_data):
        """测试分配角色给用户成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        # 创建角色
        create_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(create_response.content)

        # 分配角色
        assign_data = {"user_id": str(user.id), "role_ids": [role["role_id"]]}
        response = self.client.post(f"{self.base_url}/users/{user.id}/roles", data=json.dumps(assign_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "角色分配成功"

    def test_remove_role_from_user_success(self, user_data, role_data):
        """测试从用户移除角色成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        # 创建角色
        role = role_data.copy()
        role["name"] = "待移除角色"
        role["code"] = "remove_role"
        create_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role), content_type="application/json")
        role_resp = json.loads(create_response.content)

        # 先分配角色
        assign_data = {"user_id": str(user.id), "role_ids": [role_resp["role_id"]]}
        self.client.post(f"{self.base_url}/users/{user.id}/roles", data=json.dumps(assign_data), content_type="application/json")

        # 移除角色
        response = self.client.delete(f"{self.base_url}/users/{user.id}/roles/{role_resp['role_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "角色移除成功"

    def test_get_user_roles_success(self, user_data):
        """测试获取用户角色成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.get(f"{self.base_url}/users/{user.id}/roles")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "roles" in data

    def test_check_user_permission_success(self, user_data):
        """测试检查用户权限"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.get(f"{self.base_url}/users/{user.id}/permissions/check?permission_code=user:view")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "has_permission" in data
