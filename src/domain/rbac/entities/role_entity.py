"""
角色实体
Role Entity - RBAC核心实体
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RoleEntity:
    """
    角色实体
    RBAC权限管理核心实体
    """

    role_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    code: str = ""  # 角色代码，如 'admin', 'user', 'moderator'
    description: str = ""
    permissions: list[str] = field(default_factory=list)  # 权限代码列表
    is_system: bool = False  # 是否系统角色（不可删除）
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str | None = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("角色名称不能为空")
        if not self.code:
            raise ValueError("角色代码不能为空")

    def add_permission(self, permission_code: str) -> None:
        """添加权限"""
        if permission_code not in self.permissions:
            self.permissions.append(permission_code)
            self.updated_at = datetime.now()

    def remove_permission(self, permission_code: str) -> None:
        """移除权限"""
        if permission_code in self.permissions:
            self.permissions.remove(permission_code)
            self.updated_at = datetime.now()

    def has_permission(self, permission_code: str) -> bool:
        """检查是否拥有指定权限"""
        return permission_code in self.permissions

    def clear_permissions(self) -> None:
        """清空所有权限"""
        self.permissions = []
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """激活角色"""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """停用角色"""
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "role_id": self.role_id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "permissions": self.permissions,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
        }
