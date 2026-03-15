"""
系统管理 API 测试
"""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestSystemAPI:
    """系统管理 API 测试"""

    def setup_method(self):
        """测试方法设置"""
        from django.contrib.auth import get_user_model

        self.client = Client()
        self.base_url = "/api/v1/system"
        self.User = get_user_model()

    # ========== 健康检查测试 ==========

    def test_health_check_success(self):
        """测试健康检查成功"""
        response = self.client.get(f"{self.base_url}/health")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["status"] == "ok"

    # ========== 部门管理测试 ==========

    def test_create_dept_success(self):
        """测试创建部门成功"""
        dept_data = {"name": "技术部", "code": "tech", "sort": 1, "is_active": True}
        response = self.client.post(f"{self.base_url}/depts", data=json.dumps(dept_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "技术部"

    def test_get_dept_success(self):
        """测试获取部门详情成功"""
        # 先创建部门
        dept_data = {"name": "测试部门", "code": "test_dept", "sort": 1}
        create_response = self.client.post(f"{self.base_url}/depts", data=json.dumps(dept_data), content_type="application/json")
        dept = json.loads(create_response.content)

        response = self.client.get(f"{self.base_url}/depts/{dept['dept_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "测试部门"

    def test_get_dept_not_found(self):
        """测试获取不存在的部门"""
        response = self.client.get(f"{self.base_url}/depts/99999")
        assert response.status_code == 500

    def test_list_depts_success(self):
        """测试获取部门列表成功"""
        # 创建多个部门
        for i in range(3):
            dept_data = {"name": f"部门{i}", "code": f"dept_{i}", "sort": i}
            self.client.post(f"{self.base_url}/depts", data=json.dumps(dept_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/depts")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "depts" in data
        assert "total" in data

    def test_get_dept_tree_success(self):
        """测试获取部门树形结构成功"""
        # 创建父部门
        parent_data = {"name": "父部门", "code": "parent_dept", "sort": 1}
        parent_response = self.client.post(f"{self.base_url}/depts", data=json.dumps(parent_data), content_type="application/json")
        parent = json.loads(parent_response.content)

        # 创建子部门
        child_data = {"name": "子部门", "code": "child_dept", "parent_id": parent["dept_id"], "sort": 1}
        self.client.post(f"{self.base_url}/depts", data=json.dumps(child_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/depts/tree")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_update_dept_success(self):
        """测试更新部门成功"""
        # 先创建部门
        dept_data = {"name": "待更新部门", "code": "update_dept", "sort": 1}
        create_response = self.client.post(f"{self.base_url}/depts", data=json.dumps(dept_data), content_type="application/json")
        dept = json.loads(create_response.content)

        update_data = {"name": "更新后的部门"}
        response = self.client.put(f"{self.base_url}/depts/{dept['dept_id']}", data=json.dumps(update_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "更新后的部门"

    def test_delete_dept_success(self):
        """测试删除部门成功"""
        # 先创建部门
        dept_data = {"name": "待删除部门", "code": "delete_dept", "sort": 1}
        create_response = self.client.post(f"{self.base_url}/depts", data=json.dumps(dept_data), content_type="application/json")
        dept = json.loads(create_response.content)

        response = self.client.delete(f"{self.base_url}/depts/{dept['dept_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "部门删除成功"

    # ========== 菜单管理测试 ==========

    def test_create_menu_success(self):
        """测试创建菜单成功"""
        menu_data = {"name": "系统管理", "path": "/system", "component": "Layout", "menu_type": 0, "sort": 1, "is_active": True}
        response = self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "系统管理"

    def test_get_menu_success(self):
        """测试获取菜单详情成功"""
        # 先创建菜单
        menu_data = {"name": "测试菜单", "path": "/test", "component": "Test", "menu_type": 1, "sort": 1}
        create_response = self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")
        menu = json.loads(create_response.content)

        response = self.client.get(f"{self.base_url}/menus/{menu['menu_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "测试菜单"

    def test_list_menus_success(self):
        """测试获取菜单列表成功"""
        # 创建多个菜单
        for i in range(3):
            menu_data = {"name": f"菜单{i}", "path": f"/menu{i}", "component": f"Menu{i}", "menu_type": 1, "sort": i}
            self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/menus")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "menus" in data
        assert "total" in data

    def test_get_menu_tree_success(self):
        """测试获取菜单树形结构成功"""
        # 创建父菜单
        parent_data = {"name": "父菜单", "path": "/parent", "component": "Layout", "menu_type": 0, "sort": 1}
        parent_response = self.client.post(f"{self.base_url}/menus", data=json.dumps(parent_data), content_type="application/json")
        parent = json.loads(parent_response.content)

        # 创建子菜单
        child_data = {"name": "子菜单", "path": "/parent/child", "component": "Child", "menu_type": 1, "parent_id": parent["menu_id"], "sort": 1}
        self.client.post(f"{self.base_url}/menus", data=json.dumps(child_data), content_type="application/json")

        response = self.client.get(f"{self.base_url}/menus/tree")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_update_menu_success(self):
        """测试更新菜单成功"""
        # 先创建菜单
        menu_data = {"name": "待更新菜单", "path": "/update", "component": "Update", "menu_type": 1, "sort": 1}
        create_response = self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")
        menu = json.loads(create_response.content)

        update_data = {"name": "更新后的菜单"}
        response = self.client.put(f"{self.base_url}/menus/{menu['menu_id']}", data=json.dumps(update_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "更新后的菜单"

    def test_delete_menu_success(self):
        """测试删除菜单成功"""
        # 先创建菜单
        menu_data = {"name": "待删除菜单", "path": "/delete", "component": "Delete", "menu_type": 1, "sort": 1}
        create_response = self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")
        menu = json.loads(create_response.content)

        response = self.client.delete(f"{self.base_url}/menus/{menu['menu_id']}")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "菜单删除成功"

    # ========== 角色管理测试 ==========

    def test_system_create_role_success(self):
        """测试系统模块创建角色成功"""
        role_data = {"name": "系统角色", "code": "sys_role", "description": "系统模块角色", "sort": 1}
        response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["name"] == "系统角色"

    def test_system_list_roles_success(self):
        """测试系统模块获取角色列表成功"""
        response = self.client.get(f"{self.base_url}/roles")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "roles" in data
        assert "total" in data

    def test_assign_menus_to_role_success(self):
        """测试为角色分配菜单权限成功"""
        # 创建菜单
        menu_data = {"name": "权限菜单", "path": "/permission", "component": "Permission", "menu_type": 1, "sort": 1}
        menu_response = self.client.post(f"{self.base_url}/menus", data=json.dumps(menu_data), content_type="application/json")
        menu = json.loads(menu_response.content)

        # 创建角色
        role_data = {"name": "权限角色", "code": "perm_role", "sort": 1}
        role_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(role_response.content)

        # 分配菜单
        assign_data = {"menu_ids": [menu["menu_id"]]}
        response = self.client.post(f"{self.base_url}/roles/{role['role_id']}/menus", data=json.dumps(assign_data), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "菜单权限分配成功"

    def test_get_role_menus_success(self):
        """测试获取角色菜单成功"""
        # 创建角色
        role_data = {"name": "菜单角色", "code": "menu_role", "sort": 1}
        role_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(role_response.content)

        response = self.client.get(f"{self.base_url}/roles/{role['role_id']}/menus")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "menus" in data

    # ========== 用户角色管理测试 ==========

    def test_assign_roles_to_user_success(self, user_data):
        """测试为用户分配角色成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        # 创建角色
        role_data = {"name": "用户角色", "code": "user_role", "sort": 1}
        role_response = self.client.post(f"{self.base_url}/roles", data=json.dumps(role_data), content_type="application/json")
        role = json.loads(role_response.content)

        # 分配角色
        response = self.client.post(f"{self.base_url}/users/{user.id}/roles", data=json.dumps([role["role_id"]]), content_type="application/json")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "角色分配成功"

    def test_get_user_roles_system_success(self, user_data):
        """测试系统模块获取用户角色成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.get(f"{self.base_url}/users/{user.id}/roles")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "roles" in data

    def test_get_user_menus_success(self, user_data):
        """测试获取用户菜单权限成功"""
        # 创建用户
        user = self.User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])

        response = self.client.get(f"{self.base_url}/users/{user.id}/menus")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "menus" in data

    # ========== 操作日志测试 ==========

    def test_list_operation_logs_success(self):
        """测试获取操作日志列表成功"""
        response = self.client.get(f"{self.base_url}/operation-logs")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "logs" in data
        assert "total" in data

    def test_list_operation_logs_with_filter(self):
        """测试带过滤条件获取操作日志"""
        response = self.client.get(f"{self.base_url}/operation-logs?module=auth&method=POST&page=1&page_size=10")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "logs" in data
        assert "total" in data

    def test_get_operation_log_not_found(self):
        """测试获取不存在的操作日志"""
        response = self.client.get(f"{self.base_url}/operation-logs/99999")
        assert response.status_code == 500
