"""
认证模型
Auth Models - Django ORM模型定义
"""

import uuid

from django.conf import settings
from django.db import models


class RefreshToken(models.Model):
    """
    刷新令牌模型
    用于JWT Token刷新
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refresh_tokens", verbose_name="用户")
    token = models.CharField(max_length=500, unique=True, db_index=True, verbose_name="刷新令牌")
    jti = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="JWT ID")
    device_info = models.CharField(max_length=255, blank=True, null=True, verbose_name="设备信息")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP地址")
    is_revoked = models.BooleanField(default=False, verbose_name="是否撤销")
    expires_at = models.DateTimeField(verbose_name="过期时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "refresh_tokens"
        verbose_name = "刷新令牌"
        verbose_name_plural = "刷新令牌"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user"]), models.Index(fields=["jti"])]

    def __str__(self):
        return f"{self.user.username} - {self.jti}"


class TokenBlacklist(models.Model):
    """
    Token黑名单模型
    存储已撤销的Token
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jti = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="JWT ID")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blacklisted_tokens", verbose_name="用户")
    token_type = models.CharField(max_length=20, choices=[("access", "访问令牌"), ("refresh", "刷新令牌")], verbose_name="令牌类型")
    revoked_at = models.DateTimeField(auto_now_add=True, verbose_name="撤销时间")
    expires_at = models.DateTimeField(verbose_name="原过期时间")

    class Meta:
        db_table = "token_blacklist"
        verbose_name = "Token黑名单"
        verbose_name_plural = "Token黑名单"
        ordering = ["-revoked_at"]

    def __str__(self):
        return f"{self.user.username} - {self.jti}"


class LoginLog(models.Model):
    """
    登录日志模型
    记录用户登录信息
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_logs", verbose_name="用户")
    username = models.CharField(max_length=150, verbose_name="用户名")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(blank=True, null=True, verbose_name="用户代理")
    device_info = models.CharField(max_length=255, blank=True, null=True, verbose_name="设备信息")
    browser = models.CharField(max_length=100, blank=True, null=True, verbose_name="浏览器")
    os = models.CharField(max_length=100, blank=True, null=True, verbose_name="操作系统")
    login_status = models.BooleanField(default=True, verbose_name="登录状态")
    fail_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name="失败原因")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="登录时间")

    class Meta:
        db_table = "login_logs"
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志"
        ordering = ["-login_time"]
        indexes = [models.Index(fields=["user"]), models.Index(fields=["login_time"])]

    def __str__(self):
        return f"{self.username} - {self.login_time}"
