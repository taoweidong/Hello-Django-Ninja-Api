"""
RBAC仓储接口定义
RBAC Repository Interface - 定义角色和权限数据访问契约
"""

from abc import ABC, abstractmethod

from src.domain.rbac.entities.permission_entity import PermissionEntity
from src.domain.rbac.entities.role_entity import RoleEntity


class RBACRepositoryInterface(ABC):
    """
    RBAC仓储接口定义
    - 角色数据访问
    - 权限数据访问
    - 用户角色关联
    """

    # ========== 角色操作 ==========

    @abstractmethod
    async def get_role_by_id(self, role_id: str) -> RoleEntity | None:
        """根据ID获取角色"""
        pass

    @abstractmethod
    async def get_role_by_code(self, code: str) -> RoleEntity | None:
        """根据角色代码获取角色"""
        pass

    @abstractmethod
    async def save_role(self, role: RoleEntity) -> RoleEntity:
        """保存角色"""
        pass

    @abstractmethod
    async def update_role(self, role: RoleEntity) -> RoleEntity:
        """更新角色"""
        pass

    @abstractmethod
    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        pass

    @abstractmethod
    async def list_roles(self, is_active: bool = None) -> list[RoleEntity]:
        """获取角色列表"""
        pass

    # ========== 权限操作 ==========

    @abstractmethod
    async def get_permission_by_id(self, permission_id: str) -> PermissionEntity | None:
        """根据ID获取权限"""
        pass

    @abstractmethod
    async def get_permission_by_code(self, code: str) -> PermissionEntity | None:
        """根据权限代码获取权限"""
        pass

    @abstractmethod
    async def save_permission(self, permission: PermissionEntity) -> PermissionEntity:
        """保存权限"""
        pass

    @abstractmethod
    async def update_permission(self, permission: PermissionEntity) -> PermissionEntity:
        """更新权限"""
        pass

    @abstractmethod
    async def delete_permission(self, permission_id: str) -> bool:
        """删除权限"""
        pass

    @abstractmethod
    async def list_permissions(
        self, is_active: bool = None, resource: str = None
    ) -> list[PermissionEntity]:
        """获取权限列表"""
        pass

    # ========== 用户角色关联 ==========

    @abstractmethod
    async def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """分配角色给用户"""
        pass

    @abstractmethod
    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        pass

    @abstractmethod
    async def get_user_roles(self, user_id: str) -> list[RoleEntity]:
        """获取用户的所有角色"""
        pass

    @abstractmethod
    async def get_user_permissions(self, user_id: str) -> list[PermissionEntity]:
        """获取用户的所有权限"""
        pass

    @abstractmethod
    async def has_permission(self, user_id: str, permission_code: str) -> bool:
        """检查用户是否拥有指定权限"""
        pass
