"""
RBAC 模型测试
"""

import pytest


class TestRoleModel:
    """角色模型测试"""

    def setup_method(self):
        """测试方法设置"""
        from src.infrastructure.persistence.models.rbac_models import Role

        self.Role = Role

    @pytest.mark.django_db
    def test_create_role_success(self, role_data):
        """测试创建角色成功"""
        role = self.Role.objects.create(**role_data)
        assert role.name == role_data["name"]
        assert role.code == role_data["code"]
        assert role.description == role_data["description"]
        assert role.is_active

    @pytest.mark.django_db
    def test_role_str_representation(self, role_data):
        """测试角色字符串表示"""
        role = self.Role.objects.create(**role_data)
        assert str(role) == role.name

    @pytest.mark.django_db
    def test_role_unique_code(self, role_data):
        """测试角色代码唯一性"""
        self.Role.objects.create(**role_data)
        with pytest.raises(Exception):
            self.Role.objects.create(**role_data)


class TestPermissionModel:
    """权限模型测试"""

    def setup_method(self):
        """测试方法设置"""
        from src.infrastructure.persistence.models.rbac_models import Permission

        self.Permission = Permission

    @pytest.mark.django_db
    def test_create_permission_success(self, permission_data):
        """测试创建权限成功"""
        permission = self.Permission.objects.create(**permission_data)
        assert permission.name == permission_data["name"]
        assert permission.code == permission_data["code"]
        assert permission.resource == permission_data["resource"]
        assert permission.action == permission_data["action"]

    @pytest.mark.django_db
    def test_permission_str_representation(self, permission_data):
        """测试权限字符串表示"""
        permission = self.Permission.objects.create(**permission_data)
        assert str(permission) == f"{permission.name} ({permission.code})"


class TestRolePermissionModel:
    """角色权限关联测试"""

    def setup_method(self):
        """测试方法设置"""
        from src.infrastructure.persistence.models.rbac_models import Permission, Role

        self.Role = Role
        self.Permission = Permission

    @pytest.mark.django_db
    def test_assign_permission_to_role(self, role_data, permission_data):
        """测试为角色分配权限"""
        role = self.Role.objects.create(**role_data)
        permission = self.Permission.objects.create(**permission_data)

        # 使用多对多关系添加权限
        role.permissions.add(permission)

        assert permission in role.permissions.all()

    @pytest.mark.django_db
    def test_revoke_permission_from_role(self, role_data, permission_data):
        """测试撤销角色权限"""
        role = self.Role.objects.create(**role_data)
        permission = self.Permission.objects.create(**permission_data)

        # 添加权限
        role.permissions.add(permission)
        assert permission in role.permissions.all()

        # 移除权限
        role.permissions.remove(permission)
        assert permission not in role.permissions.all()
