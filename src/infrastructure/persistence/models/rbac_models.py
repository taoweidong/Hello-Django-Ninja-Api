"""
RBAC模型
RBAC Models - Django ORM模型定义
"""

import uuid

from django.db import models

from src.infrastructure.persistence.models.user_models import User


class Permission(models.Model):
    """
    权限模型
    定义系统操作的访问许可
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="权限代码")
    name = models.CharField(max_length=100, verbose_name="权限名称")
    resource = models.CharField(max_length=50, db_index=True, verbose_name="资源类型")
    action = models.CharField(max_length=50, verbose_name="操作类型")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "permissions"
        verbose_name = "权限"
        verbose_name_plural = "权限"
        ordering = ["resource", "action"]
        indexes = [models.Index(fields=["resource"]), models.Index(fields=["code"])]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Role(models.Model):
    """
    角色模型
    RBAC权限管理核心实体
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="角色代码")
    name = models.CharField(max_length=100, verbose_name="角色名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True, verbose_name="权限")
    is_system = models.BooleanField(default=False, verbose_name="系统角色")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_roles", verbose_name="创建者")

    class Meta:
        db_table = "roles"
        verbose_name = "角色"
        verbose_name_plural = "角色"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    用户角色关联模型
    实现用户与角色的多对多关系
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles", verbose_name="用户")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles", verbose_name="角色")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="分配时间")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_roles", verbose_name="分配者")

    class Meta:
        db_table = "user_roles"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"
        unique_together = [["user", "role"]]
        indexes = [models.Index(fields=["user"]), models.Index(fields=["role"])]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class RolePermissionHistory(models.Model):
    """
    角色权限变更历史
    记录角色权限的变更记录
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permission_history", verbose_name="角色")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name="权限")
    action = models.CharField(max_length=20, choices=[("add", "添加"), ("remove", "移除")], verbose_name="操作类型")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="变更时间")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="permission_changes", verbose_name="变更者")

    class Meta:
        db_table = "role_permission_history"
        verbose_name = "角色权限变更历史"
        verbose_name_plural = "角色权限变更历史"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.role.name} - {self.permission.name} - {self.action}"
