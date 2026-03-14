"""
RBAC控制器
RBAC Controller - 角色权限管理API控制器
"""

from src.application.dto.rbac import (
    AssignRoleDTO,
    PermissionResponseDTO,
    RoleCreateDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
    UserRolesResponseDTO,
)
from src.application.services.rbac_service import RBACService


class RBACController:
    """
    RBAC控制器
    处理角色权限管理相关API请求
    """

    def __init__(self, rbac_service: RBACService = None):
        self._rbac_service = rbac_service or RBACService()

    # ========== 角色管理 ==========

    async def create_role(self, role_dto: RoleCreateDTO, created_by: str = None) -> RoleResponseDTO:
        """创建角色"""
        return await self._rbac_service.create_role(role_dto, created_by)

    async def get_role(self, role_id: str) -> RoleResponseDTO:
        """获取角色详情"""
        role = await self._rbac_service.get_role(role_id)
        if not role:
            raise ValueError("角色不存在")
        return role

    async def list_roles(self, is_active: bool = None) -> list[RoleResponseDTO]:
        """获取角色列表"""
        return await self._rbac_service.list_roles(is_active)

    async def update_role(self, role_id: str, role_dto: RoleUpdateDTO) -> RoleResponseDTO:
        """更新角色"""
        return await self._rbac_service.update_role(role_id, role_dto)

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        return await self._rbac_service.delete_role(role_id)

    # ========== 权限管理 ==========

    async def create_permission(
        self, name: str, code: str, description: str = ""
    ) -> PermissionResponseDTO:
        """创建权限"""
        return await self._rbac_service.create_permission(name, code, description)

    async def list_permissions(
        self, is_active: bool = None, resource: str = None
    ) -> list[PermissionResponseDTO]:
        """获取权限列表"""
        return await self._rbac_service.list_permissions(is_active, resource)

    async def initialize_system_permissions(self) -> list[PermissionResponseDTO]:
        """初始化系统权限"""
        return await self._rbac_service.initialize_system_permissions()

    # ========== 用户角色关联 ==========

    async def assign_role_to_user(self, assign_dto: AssignRoleDTO, assigned_by: str = None) -> bool:
        """分配角色给用户"""
        return await self._rbac_service.assign_role_to_user(assign_dto, assigned_by)

    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        result = await self._rbac_service.remove_role_from_user(user_id, role_id)
        if not result:
            raise ValueError("用户没有此角色")
        return result

    async def get_user_roles(self, user_id: str) -> UserRolesResponseDTO:
        """获取用户角色权限"""
        return await self._rbac_service.get_user_roles(user_id)

    async def check_user_permission(self, user_id: str, permission_code: str) -> bool:
        """检查用户权限"""
        return await self._rbac_service.check_user_permission(user_id, permission_code)
