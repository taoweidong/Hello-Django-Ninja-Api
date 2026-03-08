"""
权限实体
Permission Entity - RBAC权限实体
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PermissionEntity:
    """
    权限实体
    定义系统操作的访问许可
    """

    permission_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    code: str = ""  # 权限代码，如 'user:read', 'user:write', 'user:delete'
    resource: str = ""  # 资源类型，如 'user', 'order', 'product'
    action: str = ""  # 操作类型，如 'read', 'write', 'delete'
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.name:
            raise ValueError("权限名称不能为空")
        if not self.code:
            raise ValueError("权限代码不能为空")
        # 自动从code解析resource和action
        if ":" in self.code and not self.resource:
            parts = self.code.split(":")
            self.resource = parts[0]
            self.action = parts[1] if len(parts) > 1 else ""

    def activate(self) -> None:
        """激活权限"""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """停用权限"""
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "permission_id": self.permission_id,
            "name": self.name,
            "code": self.code,
            "resource": self.resource,
            "action": self.action,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# 预定义系统权限
SYSTEM_PERMISSIONS = [
    # 用户管理权限
    {"name": "查看用户", "code": "user:read", "resource": "user", "action": "read"},
    {"name": "创建用户", "code": "user:create", "resource": "user", "action": "create"},
    {"name": "更新用户", "code": "user:update", "resource": "user", "action": "update"},
    {"name": "删除用户", "code": "user:delete", "resource": "user", "action": "delete"},
    # 角色管理权限
    {"name": "查看角色", "code": "role:read", "resource": "role", "action": "read"},
    {"name": "创建角色", "code": "role:create", "resource": "role", "action": "create"},
    {"name": "更新角色", "code": "role:update", "resource": "role", "action": "update"},
    {"name": "删除角色", "code": "role:delete", "resource": "role", "action": "delete"},
    # 权限管理权限
    {"name": "查看权限", "code": "permission:read", "resource": "permission", "action": "read"},
    {"name": "管理权限", "code": "permission:manage", "resource": "permission", "action": "manage"},
    # 系统管理权限
    {"name": "系统配置", "code": "system:config", "resource": "system", "action": "config"},
    {"name": "系统日志", "code": "system:logs", "resource": "system", "action": "logs"},
    # API访问权限
    {"name": "API访问", "code": "api:access", "resource": "api", "action": "access"},
]
