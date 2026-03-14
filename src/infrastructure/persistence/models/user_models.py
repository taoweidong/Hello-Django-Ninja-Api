"""
用户模型
User Models - Django ORM模型定义
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    用户模型
    扩展Django内置User模型，支持RBAC部门管理
    """

    id = models.BigAutoField(primary_key=True)
    mode_type = models.SmallIntegerField(default=0, verbose_name="模式类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")

    # 基本信息
    avatar = models.CharField(max_length=100, blank=True, null=True, verbose_name="头像")
    nickname = models.CharField(max_length=150, blank=True, default="", verbose_name="昵称")
    gender = models.IntegerField(default=0, verbose_name="性别")
    phone = models.CharField(max_length=16, blank=True, default="", verbose_name="手机号")
    email = models.EmailField(verbose_name="邮箱")

    # 部门关系
    dept = models.ForeignKey(
        "SystemDeptInfo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="所属部门",
        db_column="dept_id",
    )
    dept_belong = models.ForeignKey(
        "SystemDeptInfo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="belong_users",
        verbose_name="归属部门",
        db_column="dept_belong_id",
    )

    # 创建者和修改者
    creator = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
        verbose_name="创建者",
        db_column="creator_id",
    )
    modifier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="modified_users",
        verbose_name="修改者",
        db_column="modifier_id",
    )

    class Meta:
        db_table = "system_userinfo"
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ["-created_time"]
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self) -> str:
        return self.username

    def get_full_name(self) -> str:
        """获取用户全名"""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """
    用户档案模型
    存储用户的扩展信息
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="用户"
    )

    # 扩展信息
    website = models.URLField(blank=True, null=True, verbose_name="个人网站")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="公司")
    occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name="职业")
    github = models.CharField(max_length=100, blank=True, null=True, verbose_name="GitHub")
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name="Twitter")

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"

    def __str__(self):
        return f"{self.user.username}的档案"


class UserDevice(models.Model):
    """
    用户设备模型
    记录用户登录的设备信息
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="devices", verbose_name="用户"
    )
    device_id = models.CharField(max_length=255, verbose_name="设备ID")
    device_name = models.CharField(max_length=255, verbose_name="设备名称")
    device_type = models.CharField(max_length=50, verbose_name="设备类型")
    browser = models.CharField(max_length=100, blank=True, null=True, verbose_name="浏览器")
    os = models.CharField(max_length=100, blank=True, null=True, verbose_name="操作系统")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    last_login = models.DateTimeField(auto_now=True, verbose_name="最后登录")

    class Meta:
        db_table = "user_devices"
        verbose_name = "用户设备"
        verbose_name_plural = "用户设备"
        unique_together = [["user", "device_id"]]

    def __str__(self):
        return f"{self.user.username} - {self.device_name}"
