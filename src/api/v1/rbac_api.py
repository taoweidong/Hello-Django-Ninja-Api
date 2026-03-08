"""
RBAC API
RBAC API - 角色权限管理相关接口
"""

from ninja import Query, Router
from pydantic import BaseModel

from src.application.dto.rbac_dto import (
    AssignRoleDTO,
    PermissionResponseDTO,
    RoleCreateDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
    UserRolesResponseDTO,
)
from src.application.services.rbac_service import rbac_service

router = Router(tags=["权限管理"])


class MessageResponse(BaseModel):
    """消息响应"""

    message: str


class RoleListResponse(BaseModel):
    """角色列表响应"""

    roles: list[RoleResponseDTO]
    total: int


class PermissionListResponse(BaseModel):
    """权限列表响应"""

    permissions: list[PermissionResponseDTO]
    total: int


# ========== 角色管理 ==========


@router.post("/roles", response=RoleResponseDTO, summary="创建角色")
async def create_role(role_dto: RoleCreateDTO):
    """
    创建角色
    - 创建新的角色并分配权限
    """
    try:
        result = await rbac_service.create_role(role_dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/roles/{role_id}", response=RoleResponseDTO, summary="获取角色详情")
async def get_role(role_id: str):
    """
    获取角色详情
    - 根据角色ID获取角色信息
    """
    role = await rbac_service.get_role(role_id)
    if not role:
        raise ValueError("角色不存在")
    return role


@router.get("/roles", response=RoleListResponse, summary="获取角色列表")
async def list_roles(is_active: bool | None = Query(None)):
    """
    获取角色列表
    - 获取所有角色
    """
    roles = await rbac_service.list_roles(is_active)
    return RoleListResponse(roles=roles, total=len(roles))


@router.put("/roles/{role_id}", response=RoleResponseDTO, summary="更新角色")
async def update_role(role_id: str, role_dto: RoleUpdateDTO):
    """
    更新角色
    - 更新角色信息和权限
    """
    try:
        result = await rbac_service.update_role(role_id, role_dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.delete("/roles/{role_id}", response=MessageResponse, summary="删除角色")
async def delete_role(role_id: str):
    """
    删除角色
    - 删除指定角色
    """
    try:
        await rbac_service.delete_role(role_id)
        return MessageResponse(message="角色删除成功")
    except ValueError as e:
        raise ValueError(str(e))


# ========== 权限管理 ==========


@router.get("/permissions", response=PermissionListResponse, summary="获取权限列表")
async def list_permissions(
    is_active: bool | None = Query(None), resource: str | None = Query(None)
):
    """
    获取权限列表
    - 获取所有权限
    """
    permissions = await rbac_service.list_permissions(is_active, resource)
    return PermissionListResponse(permissions=permissions, total=len(permissions))


@router.post("/permissions/init", response=MessageResponse, summary="初始化系统权限")
async def init_permissions():
    """
    初始化系统权限
    - 创建系统预定义权限
    """
    await rbac_service.initialize_system_permissions()
    return MessageResponse(message="系统权限初始化成功")


# ========== 用户角色关联 ==========


@router.post("/users/{user_id}/roles", response=MessageResponse, summary="分配角色给用户")
async def assign_role_to_user(user_id: str, assign_dto: AssignRoleDTO):
    """
    分配角色给用户
    - 为用户分配角色
    """
    _ = user_id  # 保留参数以保持路由一致性，实际使用 assign_dto.user_id
    try:
        await rbac_service.assign_role_to_user(assign_dto)
        return MessageResponse(message="角色分配成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.delete(
    "/users/{user_id}/roles/{role_id}", response=MessageResponse, summary="从用户移除角色"
)
async def remove_role_from_user(user_id: str, role_id: str):
    """
    从用户移除角色
    - 移除用户的指定角色
    """
    result = await rbac_service.remove_role_from_user(user_id, role_id)
    if not result:
        raise ValueError("用户没有此角色")
    return MessageResponse(message="角色移除成功")


@router.get("/users/{user_id}/roles", response=UserRolesResponseDTO, summary="获取用户角色权限")
async def get_user_roles(user_id: str):
    """
    获取用户角色权限
    - 获取用户的所有角色和权限
    """
    result = await rbac_service.get_user_roles(user_id)
    return result


@router.get("/users/{user_id}/permissions/check", summary="检查用户权限")
async def check_user_permission(user_id: str, permission_code: str):
    """
    检查用户权限
    - 检查用户是否拥有指定权限
    """
    has_permission = await rbac_service.check_user_permission(user_id, permission_code)
    return {
        "user_id": user_id,
        "permission_code": permission_code,
        "has_permission": has_permission,
    }
