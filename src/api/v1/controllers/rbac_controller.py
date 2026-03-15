"""
RBAC控制器
RBAC Controller - 角色权限管理API控制器
"""

from typing import Annotated

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import AllowAny

from src.api.common.responses import MessageResponse
from src.application.dto.rbac import AssignRoleDTO, PermissionResponseDTO, RoleCreateDTO, RoleResponseDTO, RoleUpdateDTO, UserRolesResponseDTO
from src.application.services.rbac_service import RBACService


class RoleListResponse(MessageResponse):
    """角色列表响应"""

    roles: list[RoleResponseDTO]
    total: int


class PermissionListResponse(MessageResponse):
    """权限列表响应"""

    permissions: list[PermissionResponseDTO]
    total: int


@api_controller("/v1/rbac", tags=["权限管理"], permissions=[AllowAny])
class RBACController:
    """
    RBAC控制器
    处理角色权限管理相关API请求

    遵循SOLID原则:
    - 单一职责: 只处理角色权限相关的HTTP请求
    - 依赖倒置: 通过构造函数注入 RBACService
    """

    def __init__(self, rbac_service: RBACService | None = None) -> None:
        """
        初始化RBAC控制器

        Args:
            rbac_service: RBAC服务实例（可选，用于依赖注入）
        """
        self._rbac_service = rbac_service or RBACService()

    # ========== 角色管理 ==========

    @http_post("/roles", response=RoleResponseDTO, summary="创建角色", operation_id="rbac_create_role")
    async def create_role(self, role_dto: RoleCreateDTO) -> RoleResponseDTO:
        """
        创建角色

        - 创建新的角色并分配权限

        Args:
            role_dto: 角色创建数据传输对象

        Returns:
            RoleResponseDTO: 创建的角色信息

        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._rbac_service.create_role(role_dto)
        return result

    @http_get("/roles/{role_id}", response=RoleResponseDTO, summary="获取角色详情", operation_id="rbac_get_role")
    async def get_role(self, role_id: str) -> RoleResponseDTO:
        """
        获取角色详情

        - 根据角色ID获取角色信息

        Args:
            role_id: 角色ID

        Returns:
            RoleResponseDTO: 角色信息

        Raises:
            ValueError: 角色不存在时抛出
        """
        role = await self._rbac_service.get_role(role_id)
        if not role:
            raise ValueError("角色不存在")
        return role

    @http_get("/roles", response=RoleListResponse, summary="获取角色列表", operation_id="rbac_list_roles")
    async def list_roles(self, is_active: Annotated[bool | None, Query()] = None) -> RoleListResponse:
        """
        获取角色列表

        - 获取所有角色

        Args:
            is_active: 是否激活（可选过滤条件）

        Returns:
            RoleListResponse: 角色列表响应
        """
        roles = await self._rbac_service.list_roles(is_active)
        return RoleListResponse(message="获取成功", roles=roles, total=len(roles))

    @http_put("/roles/{role_id}", response=RoleResponseDTO, summary="更新角色", operation_id="rbac_update_role")
    async def update_role(self, role_id: str, role_dto: RoleUpdateDTO) -> RoleResponseDTO:
        """
        更新角色

        - 更新角色信息和权限

        Args:
            role_id: 角色ID
            role_dto: 角色更新数据传输对象

        Returns:
            RoleResponseDTO: 更新后的角色信息

        Raises:
            ValueError: 更新失败时抛出
        """
        result = await self._rbac_service.update_role(role_id, role_dto)
        return result

    @http_delete("/roles/{role_id}", response=MessageResponse, summary="删除角色", operation_id="rbac_delete_role")
    async def delete_role(self, role_id: str) -> MessageResponse:
        """
        删除角色

        - 删除指定角色

        Args:
            role_id: 角色ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 删除失败时抛出
        """
        await self._rbac_service.delete_role(role_id)
        return MessageResponse(message="角色删除成功")

    # ========== 权限管理 ==========

    @http_get("/permissions", response=PermissionListResponse, summary="获取权限列表", operation_id="rbac_list_permissions")
    async def list_permissions(
        self, is_active: Annotated[bool | None, Query()] = None, resource: Annotated[str | None, Query()] = None
    ) -> PermissionListResponse:
        """
        获取权限列表

        - 获取所有权限

        Args:
            is_active: 是否激活（可选过滤条件）
            resource: 资源类型（可选过滤条件）

        Returns:
            PermissionListResponse: 权限列表响应
        """
        permissions = await self._rbac_service.list_permissions(is_active, resource)
        return PermissionListResponse(message="获取成功", permissions=permissions, total=len(permissions))

    @http_post("/permissions/init", response=MessageResponse, summary="初始化系统权限", operation_id="rbac_init_permissions")
    async def init_permissions(self) -> MessageResponse:
        """
        初始化系统权限

        - 创建系统预定义权限

        Returns:
            MessageResponse: 操作结果消息
        """
        await self._rbac_service.initialize_system_permissions()
        return MessageResponse(message="系统权限初始化成功")

    # ========== 用户角色关联 ==========

    @http_post("/users/{user_id}/roles", response=MessageResponse, summary="分配角色给用户", operation_id="rbac_assign_role")
    async def assign_role_to_user(self, user_id: str, assign_dto: AssignRoleDTO) -> MessageResponse:
        """
        分配角色给用户

        - 为用户分配角色

        Args:
            user_id: 用户ID（路由参数，实际使用 assign_dto.user_id）
            assign_dto: 角色分配数据传输对象

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 分配失败时抛出
        """
        _ = user_id  # 保留参数以保持路由一致性
        await self._rbac_service.assign_role_to_user(assign_dto)
        return MessageResponse(message="角色分配成功")

    @http_delete("/users/{user_id}/roles/{role_id}", response=MessageResponse, summary="从用户移除角色", operation_id="rbac_remove_role")
    async def remove_role_from_user(self, user_id: str, role_id: str) -> MessageResponse:
        """
        从用户移除角色

        - 移除用户的指定角色

        Args:
            user_id: 用户ID
            role_id: 角色ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 移除失败时抛出
        """
        result = await self._rbac_service.remove_role_from_user(user_id, role_id)
        if not result:
            raise ValueError("用户没有此角色")
        return MessageResponse(message="角色移除成功")

    @http_get("/users/{user_id}/roles", response=UserRolesResponseDTO, summary="获取用户角色权限", operation_id="rbac_get_user_roles")
    async def get_user_roles(self, user_id: str) -> UserRolesResponseDTO:
        """
        获取用户角色权限

        - 获取用户的所有角色和权限

        Args:
            user_id: 用户ID

        Returns:
            UserRolesResponseDTO: 用户角色权限信息
        """
        result = await self._rbac_service.get_user_roles(user_id)
        return result

    @http_get("/users/{user_id}/permissions/check", summary="检查用户权限", operation_id="rbac_check_permission")
    async def check_user_permission(self, user_id: str, permission_code: Annotated[str, Query()]) -> dict:
        """
        检查用户权限

        - 检查用户是否拥有指定权限

        Args:
            user_id: 用户ID
            permission_code: 权限代码

        Returns:
            dict: 包含检查结果的字典
        """
        has_permission = await self._rbac_service.check_user_permission(user_id, permission_code)
        return {"user_id": user_id, "permission_code": permission_code, "has_permission": has_permission}
