"""
RBAC领域服务
RBAC Domain Service - 处理角色和权限相关的核心业务逻辑
"""

from src.domain.rbac.entities.permission_entity import SYSTEM_PERMISSIONS, PermissionEntity
from src.domain.rbac.entities.role_entity import RoleEntity
from src.domain.rbac.repositories.rbac_repository import RBACRepositoryInterface


class RBACDomainService:
    """
    RBAC领域服务
    处理角色和权限相关的核心业务逻辑
    """

    def __init__(self, rbac_repository: RBACRepositoryInterface):
        self.rbac_repository = rbac_repository

    # ========== 角色管理 ==========

    async def create_role(
        self,
        name: str,
        code: str,
        description: str = "",
        permissions: list[str] = None,
        created_by: str = None,
    ) -> RoleEntity:
        """创建角色"""
        # 检查角色代码是否已存在
        existing = await self.rbac_repository.get_role_by_code(code)
        if existing:
            raise ValueError(f"角色代码 {code} 已存在")

        role = RoleEntity(
            name=name,
            code=code,
            description=description,
            permissions=permissions or [],
            created_by=created_by,
        )
        return await self.rbac_repository.save_role(role)

    async def update_role(self, role_id: str, **kwargs) -> RoleEntity:
        """更新角色"""
        role = await self.rbac_repository.get_role_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")

        if role.is_system:
            raise ValueError("系统角色不可修改")

        # 更新角色属性
        if "name" in kwargs:
            role.name = kwargs["name"]
        if "description" in kwargs:
            role.description = kwargs["description"]
        if "permissions" in kwargs:
            role.permissions = kwargs["permissions"]

        return await self.rbac_repository.update_role(role)

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        role = await self.rbac_repository.get_role_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")

        if role.is_system:
            raise ValueError("系统角色不可删除")

        return await self.rbac_repository.delete_role(role_id)

    async def get_role(self, role_id: str) -> RoleEntity | None:
        """获取角色"""
        return await self.rbac_repository.get_role_by_id(role_id)

    async def list_roles(self, is_active: bool = None) -> list[RoleEntity]:
        """获取角色列表"""
        return await self.rbac_repository.list_roles(is_active)

    # ========== 权限管理 ==========

    async def create_permission(
        self, name: str, code: str, description: str = ""
    ) -> PermissionEntity:
        """创建权限"""
        existing = await self.rbac_repository.get_permission_by_code(code)
        if existing:
            raise ValueError(f"权限代码 {code} 已存在")

        permission = PermissionEntity(
            name=name,
            code=code,
            description=description,
        )
        return await self.rbac_repository.save_permission(permission)

    async def initialize_system_permissions(self) -> list[PermissionEntity]:
        """初始化系统权限"""
        created_permissions = []
        for perm_data in SYSTEM_PERMISSIONS:
            existing = await self.rbac_repository.get_permission_by_code(perm_data["code"])
            if not existing:
                permission = PermissionEntity(**perm_data)
                created = await self.rbac_repository.save_permission(permission)
                created_permissions.append(created)
        return created_permissions

    async def list_permissions(
        self, is_active: bool = None, resource: str = None
    ) -> list[PermissionEntity]:
        """获取权限列表"""
        return await self.rbac_repository.list_permissions(is_active, resource)

    # ========== 用户角色关联 ==========

    async def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """分配角色给用户"""
        role = await self.rbac_repository.get_role_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")
        if not role.is_active:
            raise ValueError("角色已被停用")

        return await self.rbac_repository.assign_role_to_user(user_id, role_id)

    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        return await self.rbac_repository.remove_role_from_user(user_id, role_id)

    async def get_user_roles(self, user_id: str) -> list[RoleEntity]:
        """获取用户的所有角色"""
        return await self.rbac_repository.get_user_roles(user_id)

    async def get_user_permissions(self, user_id: str) -> list[PermissionEntity]:
        """获取用户的所有权限"""
        return await self.rbac_repository.get_user_permissions(user_id)

    async def check_permission(self, user_id: str, permission_code: str) -> bool:
        """检查用户是否拥有指定权限"""
        return await self.rbac_repository.has_permission(user_id, permission_code)
