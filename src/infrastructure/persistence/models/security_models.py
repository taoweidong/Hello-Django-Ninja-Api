"""
安全模型
Security Models - Django ORM模型定义
"""

import uuid
from datetime import datetime

from django.conf import settings
from django.db import models


class IPBlacklist(models.Model):
    """
    IP黑名单模型
    存储被禁止访问的IP地址
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=True, db_index=True, verbose_name="IP地址")
    reason = models.TextField(blank=True, null=True, verbose_name="封禁原因")
    is_permanent = models.BooleanField(default=False, verbose_name="是否永久封禁")
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name="过期时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_blacklists",
        verbose_name="创建者",
    )

    class Meta:
        db_table = "ip_blacklist"
        verbose_name = "IP黑名单"
        verbose_name_plural = "IP黑名单"
        ordering = ["-created_at"]

    def __str__(self):
        return self.ip_address

    def is_active(self):
        """检查是否处于封禁状态"""
        if self.is_permanent:
            return True
        if self.expires_at:
            return datetime.now() < self.expires_at
        return False


class IPWhitelist(models.Model):
    """
    IP白名单模型
    存储允许访问的IP地址
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=True, db_index=True, verbose_name="IP地址")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_whitelists",
        verbose_name="创建者",
    )

    class Meta:
        db_table = "ip_whitelist"
        verbose_name = "IP白名单"
        verbose_name_plural = "IP白名单"
        ordering = ["-created_at"]

    def __str__(self):
        return self.ip_address


class RateLimitRule(models.Model):
    """
    限流规则模型
    定义API访问频率限制规则
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="规则名称")
    endpoint = models.CharField(max_length=255, db_index=True, verbose_name="API端点")
    method = models.CharField(
        max_length=10,
        choices=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("PATCH", "PATCH"),
            ("DELETE", "DELETE"),
            ("*", "ALL"),
        ],
        default="*",
        verbose_name="HTTP方法",
    )
    rate = models.PositiveIntegerField(default=60, verbose_name="允许的请求次数")
    period = models.PositiveIntegerField(default=60, verbose_name="时间周期(秒)")
    scope = models.CharField(
        max_length=20,
        choices=[
            ("ip", "IP地址"),
            ("user", "用户"),
            ("global", "全局"),
        ],
        default="ip",
        verbose_name="限流范围",
    )
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "rate_limit_rules"
        verbose_name = "限流规则"
        verbose_name_plural = "限流规则"
        ordering = ["-created_at"]
        unique_together = [["endpoint", "method"]]

    def __str__(self):
        return f"{self.name} - {self.method}:{self.endpoint}"

    def get_rate_string(self):
        """获取限流字符串"""
        if self.period >= 60:
            return f"{self.rate}/{self.period // 60}minute"
        return f"{self.rate}/{self.period}second"


class RateLimitRecord(models.Model):
    """
    限流记录模型
    记录实际请求次数
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, db_index=True, verbose_name="限流键")
    endpoint = models.CharField(max_length=255, db_index=True, verbose_name="API端点")
    method = models.CharField(max_length=10, default="GET", verbose_name="HTTP方法")
    count = models.PositiveIntegerField(default=0, verbose_name="请求次数")
    window_start = models.DateTimeField(verbose_name="窗口开始时间")
    expires_at = models.DateTimeField(verbose_name="过期时间")

    class Meta:
        db_table = "rate_limit_records"
        verbose_name = "限流记录"
        verbose_name_plural = "限流记录"
        indexes = [
            models.Index(fields=["key", "endpoint", "method"]),
        ]

    def __str__(self):
        return f"{self.key} - {self.endpoint} - {self.count}"
