"""
系统管理控制器
System Management Controller - 部门、菜单、角色、操作日志管理API控制器
"""

from datetime import datetime

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import AllowAny

from src.api.common.responses import MessageResponse
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


class DeptListResponse(MessageResponse):
    """部门列表响应"""

    depts: list[DeptResponseDTO]
    total: int


class MenuListResponse(MessageResponse):
    """菜单列表响应"""

    menus: list[MenuResponseDTO]
    total: int


class RoleListResponse(MessageResponse):
    """角色列表响应"""

    roles: list[RoleResponseDTO]
    total: int


class LogListResponse(MessageResponse):
    """操作日志列表响应"""

    logs: list[LogResponseDTO]
    total: int


@api_controller("/v1/system", tags=["系统管理"], permissions=[AllowAny])
class SystemController:
    """
    系统管理控制器
    处理部门、菜单、角色、操作日志相关API请求

    遵循SOLID原则:
    - 单一职责: 只处理系统管理相关的HTTP请求
    - 依赖倒置: 通过构造函数注入 SystemService
    """

    def __init__(self, system_service: SystemService | None = None) -> None:
        """
        初始化系统管理控制器

        Args:
            system_service: 系统服务实例（可选，用于依赖注入）
        """
        self._system_service = system_service or SystemService()

    # ========== 系统管理 ==========

    @http_get("/health", response=dict, summary="健康检查", operation_id="system_health_check")
    def health_check(self) -> dict:
        """
        健康检查

        - 检查API服务是否正常运行
        - 无需认证即可访问

        Returns:
            dict: 健康状态信息
        """
        return {"status": "ok", "message": "服务运行正常", "service": "Hello-Django-Ninja-Api", "version": "1.0.0"}

    # ========== 部门管理 ==========

    @http_post("/depts", response=DeptResponseDTO, summary="创建部门", operation_id="system_create_dept")
    async def create_dept(self, dto: DeptCreateDTO) -> DeptResponseDTO:
        """
        创建部门

        - 创建新的部门信息
        - 支持指定上级部门和归属部门

        Args:
            dto: 部门创建数据传输对象

        Returns:
            DeptResponseDTO: 创建的部门信息

        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._system_service.create_dept(dto)
        return result

    @http_get("/depts/{dept_id}", response=DeptResponseDTO, summary="获取部门详情", operation_id="system_get_dept")
    async def get_dept(self, dept_id: str) -> DeptResponseDTO:
        """
        获取部门详情

        - 根据部门ID获取部门详细信息

        Args:
            dept_id: 部门ID

        Returns:
            DeptResponseDTO: 部门信息

        Raises:
            ValueError: 部门不存在时抛出
        """
        dept = await self._system_service.get_dept(dept_id)
        if not dept:
            raise ValueError("部门不存在")
        return dept

    @http_put("/depts/{dept_id}", response=DeptResponseDTO, summary="更新部门", operation_id="system_update_dept")
    async def update_dept(self, dept_id: str, dto: DeptUpdateDTO) -> DeptResponseDTO:
        """
        更新部门

        - 更新部门信息

        Args:
            dept_id: 部门ID
            dto: 部门更新数据传输对象

        Returns:
            DeptResponseDTO: 更新后的部门信息

        Raises:
            ValueError: 更新失败时抛出
        """
        result = await self._system_service.update_dept(dept_id, dto)
        return result

    @http_delete("/depts/{dept_id}", response=MessageResponse, summary="删除部门", operation_id="system_delete_dept")
    async def delete_dept(self, dept_id: str) -> MessageResponse:
        """
        删除部门

        - 删除指定部门（不能删除有子部门或用户的部门）

        Args:
            dept_id: 部门ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 删除失败时抛出
        """
        await self._system_service.delete_dept(dept_id)
        return MessageResponse(message="部门删除成功")

    @http_get("/depts", response=DeptListResponse, summary="获取部门列表", operation_id="system_list_depts")
    async def list_depts(self, is_active: bool | None = Query(None)) -> DeptListResponse:
        """
        获取部门列表

        - 获取所有部门信息
        - 可根据激活状态过滤

        Args:
            is_active: 是否激活（可选过滤条件）

        Returns:
            DeptListResponse: 部门列表响应
        """
        depts = await self._system_service.list_depts(is_active)
        return DeptListResponse(message="获取成功", depts=depts, total=len(depts))

    @http_get("/depts/tree", response=list[DeptTreeDTO], summary="获取部门树形结构", operation_id="system_get_dept_tree")
    async def get_dept_tree(self) -> list[DeptTreeDTO]:
        """
        获取部门树形结构

        - 获取树形结构的部门信息

        Returns:
            list[DeptTreeDTO]: 部门树形结构
        """
        tree = await self._system_service.get_dept_tree()
        return tree

    # ========== 菜单管理 ==========

    @http_post("/menus", response=MenuResponseDTO, summary="创建菜单", operation_id="system_create_menu")
    async def create_menu(self, dto: MenuCreateDTO) -> MenuResponseDTO:
        """
        创建菜单/权限

        - 创建新的菜单信息
        - 支持指定父级菜单和元数据
        - 菜单类型：0-目录，1-菜单，2-按钮

        Args:
            dto: 菜单创建数据传输对象

        Returns:
            MenuResponseDTO: 创建的菜单信息

        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._system_service.create_menu(dto)
        return result

    @http_get("/menus/{menu_id}", response=MenuResponseDTO, summary="获取菜单详情", operation_id="system_get_menu")
    async def get_menu(self, menu_id: str) -> MenuResponseDTO:
        """
        获取菜单详情

        - 根据菜单ID获取菜单详细信息

        Args:
            menu_id: 菜单ID

        Returns:
            MenuResponseDTO: 菜单信息

        Raises:
            ValueError: 菜单不存在时抛出
        """
        menu = await self._system_service.get_menu(menu_id)
        if not menu:
            raise ValueError("菜单不存在")
        return menu

    @http_put("/menus/{menu_id}", response=MenuResponseDTO, summary="更新菜单", operation_id="system_update_menu")
    async def update_menu(self, menu_id: str, dto: MenuUpdateDTO) -> MenuResponseDTO:
        """
        更新菜单

        - 更新菜单信息

        Args:
            menu_id: 菜单ID
            dto: 菜单更新数据传输对象

        Returns:
            MenuResponseDTO: 更新后的菜单信息

        Raises:
            ValueError: 更新失败时抛出
        """
        result = await self._system_service.update_menu(menu_id, dto)
        return result

    @http_delete("/menus/{menu_id}", response=MessageResponse, summary="删除菜单", operation_id="system_delete_menu")
    async def delete_menu(self, menu_id: str) -> MessageResponse:
        """
        删除菜单

        - 删除指定菜单（不能删除有子菜单或被角色使用的菜单）

        Args:
            menu_id: 菜单ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 删除失败时抛出
        """
        await self._system_service.delete_menu(menu_id)
        return MessageResponse(message="菜单删除成功")

    @http_get("/menus", response=MenuListResponse, summary="获取菜单列表", operation_id="system_list_menus")
    async def list_menus(self, is_active: bool | None = Query(None)) -> MenuListResponse:
        """
        获取菜单列表

        - 获取所有菜单信息
        - 可根据激活状态过滤

        Args:
            is_active: 是否激活（可选过滤条件）

        Returns:
            MenuListResponse: 菜单列表响应
        """
        menus = await self._system_service.list_menus(is_active)
        return MenuListResponse(message="获取成功", menus=menus, total=len(menus))

    @http_get("/menus/tree", response=list[MenuTreeDTO], summary="获取菜单树形结构", operation_id="system_get_menu_tree")
    async def get_menu_tree(self) -> list[MenuTreeDTO]:
        """
        获取菜单树形结构

        - 获取树形结构的菜单信息

        Returns:
            list[MenuTreeDTO]: 菜单树形结构
        """
        tree = await self._system_service.get_menu_tree()
        return tree

    # ========== 角色管理 ==========

    @http_post("/roles", response=RoleResponseDTO, summary="创建角色", operation_id="system_create_role")
    async def create_role(self, dto: RoleCreateDTO) -> RoleResponseDTO:
        """
        创建角色

        - 创建新的角色并分配菜单权限
        - 菜单即权限，多角色权限取交集

        Args:
            dto: 角色创建数据传输对象

        Returns:
            RoleResponseDTO: 创建的角色信息

        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._system_service.create_role(dto)
        return result

    @http_get("/roles/{role_id}", response=RoleResponseDTO, summary="获取角色详情", operation_id="system_get_role")
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
        role = await self._system_service.get_role(role_id)
        if not role:
            raise ValueError("角色不存在")
        return role

    @http_put("/roles/{role_id}", response=RoleResponseDTO, summary="更新角色", operation_id="system_update_role")
    async def update_role(self, role_id: str, dto: RoleUpdateDTO) -> RoleResponseDTO:
        """
        更新角色

        - 更新角色信息

        Args:
            role_id: 角色ID
            dto: 角色更新数据传输对象

        Returns:
            RoleResponseDTO: 更新后的角色信息

        Raises:
            ValueError: 更新失败时抛出
        """
        result = await self._system_service.update_role(role_id, dto)
        return result

    @http_delete("/roles/{role_id}", response=MessageResponse, summary="删除角色", operation_id="system_delete_role")
    async def delete_role(self, role_id: str) -> MessageResponse:
        """
        删除角色

        - 删除指定角色（不能删除已被用户使用的角色）

        Args:
            role_id: 角色ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 删除失败时抛出
        """
        await self._system_service.delete_role(role_id)
        return MessageResponse(message="角色删除成功")

    @http_get("/roles", response=RoleListResponse, summary="获取角色列表", operation_id="system_list_roles")
    async def list_roles(self, is_active: bool | None = Query(None)) -> RoleListResponse:
        """
        获取角色列表

        - 获取所有角色
        - 可根据激活状态过滤

        Args:
            is_active: 是否激活（可选过滤条件）

        Returns:
            RoleListResponse: 角色列表响应
        """
        roles = await self._system_service.list_roles(is_active)
        return RoleListResponse(message="获取成功", roles=roles, total=len(roles))

    @http_post("/roles/{role_id}/menus", response=MessageResponse, summary="为角色分配菜单权限", operation_id="system_assign_menus")
    async def assign_menus_to_role(self, role_id: str, dto: RoleAssignMenuDTO) -> MessageResponse:
        """
        为角色分配菜单权限

        - 批量分配菜单权限给角色
        - 会覆盖原有的菜单权限

        Args:
            role_id: 角色ID
            dto: 菜单分配数据传输对象

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 分配失败时抛出
        """
        await self._system_service.assign_menus_to_role(role_id, dto)
        return MessageResponse(message="菜单权限分配成功")

    @http_get("/roles/{role_id}/menus", response=MenuListResponse, summary="获取角色的菜单列表", operation_id="system_get_role_menus")
    async def get_role_menus(self, role_id: str) -> MenuListResponse:
        """
        获取角色的菜单列表

        - 获取指定角色的所有菜单权限

        Args:
            role_id: 角色ID

        Returns:
            MenuListResponse: 菜单列表响应
        """
        menus = await self._system_service.get_role_menus(role_id)
        return MenuListResponse(message="获取成功", menus=menus, total=len(menus))

    # ========== 用户角色管理 ==========

    @http_post("/users/{user_id}/roles", response=MessageResponse, summary="为用户分配角色", operation_id="system_assign_user_roles")
    async def assign_roles_to_user(self, user_id: int, role_ids: list[str]) -> MessageResponse:
        """
        为用户分配角色

        - 批量分配角色给用户
        - 会覆盖原有的角色分配

        Args:
            user_id: 用户ID
            role_ids: 角色ID列表

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 分配失败时抛出
        """
        await self._system_service.assign_roles_to_user(user_id, role_ids)
        return MessageResponse(message="角色分配成功")

    @http_get("/users/{user_id}/roles", response=RoleListResponse, summary="获取用户的角色列表", operation_id="system_get_user_roles")
    async def get_user_roles(self, user_id: int) -> RoleListResponse:
        """
        获取用户的角色列表

        - 获取指定用户的所有角色

        Args:
            user_id: 用户ID

        Returns:
            RoleListResponse: 角色列表响应
        """
        roles = await self._system_service.get_user_roles(user_id)
        return RoleListResponse(message="获取成功", roles=roles, total=len(roles))

    @http_get("/users/{user_id}/menus", response=MenuListResponse, summary="获取用户的菜单权限", operation_id="system_get_user_menus")
    async def get_user_menus(self, user_id: int) -> MenuListResponse:
        """
        获取用户的菜单权限

        - 获取用户所有角色的菜单权限交集
        - 权限即菜单，多角色取交集

        Args:
            user_id: 用户ID

        Returns:
            MenuListResponse: 菜单列表响应
        """
        menus = await self._system_service.get_user_menus(user_id)
        return MenuListResponse(message="获取成功", menus=menus, total=len(menus))

    # ========== 操作日志管理 ==========

    @http_get("/operation-logs", response=LogListResponse, summary="获取操作日志列表", operation_id="system_list_logs")
    async def list_operation_logs(self, request: object) -> LogListResponse:
        """
        获取操作日志列表

        - 支持多条件过滤
        - 支持分页查询

        Args:
            request: Django HTTP请求对象

        Returns:
            LogListResponse: 操作日志列表响应
        """
        # 从请求中提取参数
        params = dict(request.GET)  # type: ignore
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
        logs, total = await self._system_service.list_operation_logs(filters)
        return LogListResponse(message="获取成功", logs=logs, total=total)

    @http_get("/operation-logs/{log_id}", response=LogResponseDTO, summary="获取操作日志详情", operation_id="system_get_log")
    async def get_operation_log(self, log_id: int) -> LogResponseDTO:
        """
        获取操作日志详情

        - 根据日志ID获取详细操作记录

        Args:
            log_id: 日志ID

        Returns:
            LogResponseDTO: 操作日志信息

        Raises:
            ValueError: 日志不存在时抛出
        """
        log = await self._system_service.get_operation_log(log_id)
        if not log:
            raise ValueError("操作日志不存在")
        return log
