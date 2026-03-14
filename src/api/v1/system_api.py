"""
系统管理API
System Management API - 部门、菜单、角色、操作日志管理接口
"""

from ninja import Router
from pydantic import BaseModel

from src.application.dto.system import (
    DeptCreateDTO,
    DeptResponseDTO,
    DeptTreeDTO,
    DeptUpdateDTO,
    LogFilterDTO,
    LogResponseDTO,
    MenuCreateDTO,
    MenuResponseDTO,
    MenuTreeDTO,
    MenuUpdateDTO,
    RoleAssignMenuDTO,
    RoleCreateDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
)
from src.application.services.system_service import SystemService

router = Router(tags=["系统管理"])

# 创建服务实例
system_service = SystemService()


# ========== 响应模型 ==========


class MessageResponse(BaseModel):
    """消息响应"""

    message: str


class DeptListResponse(BaseModel):
    """部门列表响应"""

    depts: list[DeptResponseDTO]
    total: int


class MenuListResponse(BaseModel):
    """菜单列表响应"""

    menus: list[MenuResponseDTO]
    total: int


class RoleListResponse(BaseModel):
    """角色列表响应"""

    roles: list[RoleResponseDTO]
    total: int


class LogListResponse(BaseModel):
    """操作日志列表响应"""

    logs: list[LogResponseDTO]
    total: int


# ========== 部门管理 ==========


@router.post("/depts", response=DeptResponseDTO, summary="创建部门")
async def create_dept(dto: DeptCreateDTO):
    """
    创建部门
    - 创建新的部门信息
    - 支持指定上级部门和归属部门
    """
    try:
        result = await system_service.create_dept(dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/depts/{dept_id}", response=DeptResponseDTO, summary="获取部门详情")
async def get_dept(dept_id: str):
    """
    获取部门详情
    - 根据部门ID获取部门详细信息
    """
    dept = await system_service.get_dept(dept_id)
    if not dept:
        raise ValueError("部门不存在")
    return dept


@router.put("/depts/{dept_id}", response=DeptResponseDTO, summary="更新部门")
async def update_dept(dept_id: str, dto: DeptUpdateDTO):
    """
    更新部门
    - 更新部门信息
    """
    try:
        result = await system_service.update_dept(dept_id, dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.delete("/depts/{dept_id}", response=MessageResponse, summary="删除部门")
async def delete_dept(dept_id: str):
    """
    删除部门
    - 删除指定部门（不能删除有子部门或用户的部门）
    """
    try:
        await system_service.delete_dept(dept_id)
        return MessageResponse(message="部门删除成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/depts", response=DeptListResponse, summary="获取部门列表")
async def list_depts(
    request,
    is_active: bool | None = None,
):
    """
    获取部门列表
    - 获取所有部门信息
    - 可根据激活状态过滤
    """
    depts = await system_service.list_depts(is_active)
    return DeptListResponse(depts=depts, total=len(depts))


@router.get("/depts/tree", response=list[DeptTreeDTO], summary="获取部门树形结构")
async def get_dept_tree():
    """
    获取部门树形结构
    - 获取树形结构的部门信息
    """
    tree = await system_service.get_dept_tree()
    return tree


# ========== 菜单管理 ==========


@router.post("/menus", response=MenuResponseDTO, summary="创建菜单")
async def create_menu(dto: MenuCreateDTO):
    """
    创建菜单/权限
    - 创建新的菜单信息
    - 支持指定父级菜单和元数据
    - 菜单类型：0-目录，1-菜单，2-按钮
    """
    try:
        result = await system_service.create_menu(dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/menus/{menu_id}", response=MenuResponseDTO, summary="获取菜单详情")
async def get_menu(menu_id: str):
    """
    获取菜单详情
    - 根据菜单ID获取菜单详细信息
    """
    menu = await system_service.get_menu(menu_id)
    if not menu:
        raise ValueError("菜单不存在")
    return menu


@router.put("/menus/{menu_id}", response=MenuResponseDTO, summary="更新菜单")
async def update_menu(menu_id: str, dto: MenuUpdateDTO):
    """
    更新菜单
    - 更新菜单信息
    """
    try:
        result = await system_service.update_menu(menu_id, dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.delete("/menus/{menu_id}", response=MessageResponse, summary="删除菜单")
async def delete_menu(menu_id: str):
    """
    删除菜单
    - 删除指定菜单（不能删除有子菜单或被角色使用的菜单）
    """
    try:
        await system_service.delete_menu(menu_id)
        return MessageResponse(message="菜单删除成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/menus", response=MenuListResponse, summary="获取菜单列表")
async def list_menus(
    request,
    is_active: bool | None = None,
):
    """
    获取菜单列表
    - 获取所有菜单信息
    - 可根据激活状态过滤
    """
    menus = await system_service.list_menus(is_active)
    return MenuListResponse(menus=menus, total=len(menus))


@router.get("/menus/tree", response=list[MenuTreeDTO], summary="获取菜单树形结构")
async def get_menu_tree():
    """
    获取菜单树形结构
    - 获取树形结构的菜单信息
    """
    tree = await system_service.get_menu_tree()
    return tree


# ========== 角色管理 ==========


@router.post("/roles", response=RoleResponseDTO, summary="创建角色")
async def create_role(dto: RoleCreateDTO):
    """
    创建角色
    - 创建新的角色并分配菜单权限
    - 菜单即权限，多角色权限取交集
    """
    try:
        result = await system_service.create_role(dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/roles/{role_id}", response=RoleResponseDTO, summary="获取角色详情")
async def get_role(role_id: str):
    """
    获取角色详情
    - 根据角色ID获取角色信息
    """
    role = await system_service.get_role(role_id)
    if not role:
        raise ValueError("角色不存在")
    return role


@router.put("/roles/{role_id}", response=RoleResponseDTO, summary="更新角色")
async def update_role(role_id: str, dto: RoleUpdateDTO):
    """
    更新角色
    - 更新角色信息
    """
    try:
        result = await system_service.update_role(role_id, dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.delete("/roles/{role_id}", response=MessageResponse, summary="删除角色")
async def delete_role(role_id: str):
    """
    删除角色
    - 删除指定角色（不能删除已被用户使用的角色）
    """
    try:
        await system_service.delete_role(role_id)
        return MessageResponse(message="角色删除成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/roles", response=RoleListResponse, summary="获取角色列表")
async def list_roles(
    request,
    is_active: bool | None = None,
):
    """
    获取角色列表
    - 获取所有角色
    - 可根据激活状态过滤
    """
    roles = await system_service.list_roles(is_active)
    return RoleListResponse(roles=roles, total=len(roles))


@router.post("/roles/{role_id}/menus", response=MessageResponse, summary="为角色分配菜单权限")
async def assign_menus_to_role(role_id: str, dto: RoleAssignMenuDTO):
    """
    为角色分配菜单权限
    - 批量分配菜单权限给角色
    - 会覆盖原有的菜单权限
    """
    try:
        await system_service.assign_menus_to_role(role_id, dto)
        return MessageResponse(message="菜单权限分配成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/roles/{role_id}/menus", response=MenuListResponse, summary="获取角色的菜单列表")
async def get_role_menus(role_id: str):
    """
    获取角色的菜单列表
    - 获取指定角色的所有菜单权限
    """
    menus = await system_service.get_role_menus(role_id)
    return MenuListResponse(menus=menus, total=len(menus))


# ========== 用户角色管理 ==========


@router.post("/users/{user_id}/roles", response=MessageResponse, summary="为用户分配角色")
async def assign_roles_to_user(user_id: int, role_ids: list[str]):
    """
    为用户分配角色
    - 批量分配角色给用户
    - 会覆盖原有的角色分配
    """
    try:
        await system_service.assign_roles_to_user(user_id, role_ids)
        return MessageResponse(message="角色分配成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/users/{user_id}/roles", response=RoleListResponse, summary="获取用户的角色列表")
async def get_user_roles(user_id: int):
    """
    获取用户的角色列表
    - 获取指定用户的所有角色
    """
    roles = await system_service.get_user_roles(user_id)
    return RoleListResponse(roles=roles, total=len(roles))


@router.get("/users/{user_id}/menus", response=MenuListResponse, summary="获取用户的菜单权限")
async def get_user_menus(user_id: int):
    """
    获取用户的菜单权限
    - 获取用户所有角色的菜单权限交集
    - 权限即菜单，多角色取交集
    """
    menus = await system_service.get_user_menus(user_id)
    return MenuListResponse(menus=menus, total=len(menus))


# ========== 操作日志管理 ==========


@router.get("/operation-logs", response=LogListResponse, summary="获取操作日志列表")
async def list_operation_logs(
    request,
):
    """
    获取操作日志列表
    - 支持多条件过滤
    - 支持分页查询
    """
    from datetime import datetime

    # 从请求中提取参数
    params = dict(request.GET)
    module = params.get("module", [None])[0]
    method = params.get("method", [None])[0]
    creator_id = int(params["creator_id"][0]) if "creator_id" in params else None
    start_time = params.get("start_time", [None])[0]
    end_time = params.get("end_time", [None])[0]
    response_code = int(params["response_code"][0]) if "response_code" in params else None
    page = int(params.get("page", [1])[0])
    page_size = int(params.get("page_size", [20])[0])

    filters = LogFilterDTO(
        module=module,
        method=method,
        creator_id=creator_id,
        start_time=datetime.fromisoformat(start_time) if start_time else None,
        end_time=datetime.fromisoformat(end_time) if end_time else None,
        response_code=response_code,
        page=page,
        page_size=page_size,
    )
    logs, total = await system_service.list_operation_logs(filters)
    return LogListResponse(logs=logs, total=total)


@router.get("/operation-logs/{log_id}", response=LogResponseDTO, summary="获取操作日志详情")
async def get_operation_log(log_id: int):
    """
    获取操作日志详情
    - 根据日志ID获取详细操作记录
    """
    log = await system_service.get_operation_log(log_id)
    if not log:
        raise ValueError("操作日志不存在")
    return log
