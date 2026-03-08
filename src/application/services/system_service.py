"""
系统服务
System Service - 部门、菜单、角色、操作日志业务逻辑处理
"""

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
from src.infrastructure.repositories.system_repo_impl import SystemRepository


class SystemService:
    """
    系统应用服务
    处理部门、菜单、角色、操作日志相关业务逻辑
    """

    def __init__(self) -> None:
        self.system_repo = SystemRepository()

    # ========== 部门管理 ==========

    async def create_dept(self, dto: DeptCreateDTO, creator_id: int | None = None) -> DeptResponseDTO:
        """创建部门"""
        # 检查部门编码是否已存在
        existing = await self.system_repo.get_dept_by_code(dto.code)
        if existing:
            raise ValueError(f"部门编码 {dto.code} 已存在")

        # 创建部门
        dept = await self.system_repo.create_dept(dto, creator_id)
        return await self._to_dept_response(dept)

    async def get_dept(self, dept_id: str) -> DeptResponseDTO | None:
        """获取部门详情"""
        dept = await self.system_repo.get_dept_by_id(dept_id)
        if not dept:
            return None
        return await self._to_dept_response(dept)

    async def update_dept(self, dept_id: str, dto: DeptUpdateDTO, modifier_id: int | None = None) -> DeptResponseDTO:
        """更新部门"""
        # 检查部门编码是否重复
        if dto.code:
            existing = await self.system_repo.get_dept_by_code(dto.code)
            if existing and existing.id != dept_id:
                raise ValueError(f"部门编码 {dto.code} 已存在")

        dept = await self.system_repo.update_dept(dept_id, dto, modifier_id)
        if not dept:
            raise ValueError("部门不存在")

        return await self._to_dept_response(dept)

    async def delete_dept(self, dept_id: str) -> bool:
        """删除部门"""
        # 检查是否有子部门
        children = await self.system_repo.list_depts(parent_id=dept_id)
        if children:
            raise ValueError("该部门下存在子部门，无法删除")

        # 检查是否有用户
        from src.infrastructure.persistence.models.user_models import User

        user_count = await User.objects.filter(dept_id=dept_id).acount()
        if user_count > 0:
            raise ValueError("该部门下存在用户，无法删除")

        return await self.system_repo.delete_dept(dept_id)

    async def list_depts(self, is_active: bool | None = None) -> list[DeptResponseDTO]:
        """获取部门列表"""
        depts = await self.system_repo.list_depts(is_active)
        return [await self._to_dept_response(dept) for dept in depts]

    async def get_dept_tree(self) -> list[DeptTreeDTO]:
        """获取部门树形结构"""
        depts = await self.system_repo.list_depts()
        return self._build_dept_tree(depts)

    def _build_dept_tree(self, depts: list, parent_id: str | None = None) -> list[DeptTreeDTO]:
        """构建部门树"""
        tree = []
        for dept in depts:
            if dept.parent_id == parent_id:
                children = self._build_dept_tree(depts, dept.id)
                tree.append(
                    DeptTreeDTO(
                        id=dept.id,
                        name=dept.name,
                        code=dept.code,
                        rank=dept.rank,
                        is_active=dept.is_active,
                        parent_id=dept.parent_id,
                        children=children,
                    )
                )
        return tree

    async def _to_dept_response(self, dept) -> DeptResponseDTO:
        """转换部门响应DTO"""
        parent_name = None
        if dept.parent_id:
            parent = await self.system_repo.get_dept_by_id(dept.parent_id)
            parent_name = parent.name if parent else None

        dept_belong_name = None
        if dept.dept_belong_id:
            dept_belong = await self.system_repo.get_dept_by_id(dept.dept_belong_id)
            dept_belong_name = dept_belong.name if dept_belong else None

        return DeptResponseDTO(
            id=dept.id,
            name=dept.name,
            code=dept.code,
            rank=dept.rank,
            auto_bind=dept.auto_bind,
            is_active=dept.is_active,
            description=dept.description,
            parent_id=dept.parent_id,
            parent_name=parent_name,
            dept_belong_id=dept.dept_belong_id,
            dept_belong_name=dept_belong_name,
            created_time=dept.created_time,
            updated_time=dept.updated_time,
        )

    # ========== 菜单管理 ==========

    async def create_menu(self, dto: MenuCreateDTO, creator_id: int | None = None) -> MenuResponseDTO:
        """创建菜单"""
        # 检查菜单名称是否已存在
        existing = await self.system_repo.get_menu_by_name(dto.name)
        if existing:
            raise ValueError(f"菜单名称 {dto.name} 已存在")

        # 创建菜单
        menu = await self.system_repo.create_menu(dto, creator_id)
        return await self._to_menu_response(menu)

    async def get_menu(self, menu_id: str) -> MenuResponseDTO | None:
        """获取菜单详情"""
        menu = await self.system_repo.get_menu_by_id(menu_id)
        if not menu:
            return None
        return await self._to_menu_response(menu)

    async def update_menu(self, menu_id: str, dto: MenuUpdateDTO, modifier_id: int | None = None) -> MenuResponseDTO:
        """更新菜单"""
        # 检查菜单名称是否重复
        if dto.name:
            existing = await self.system_repo.get_menu_by_name(dto.name)
            if existing and existing.id != menu_id:
                raise ValueError(f"菜单名称 {dto.name} 已存在")

        menu = await self.system_repo.update_menu(menu_id, dto, modifier_id)
        if not menu:
            raise ValueError("菜单不存在")

        return await self._to_menu_response(menu)

    async def delete_menu(self, menu_id: str) -> bool:
        """删除菜单"""
        # 检查是否有子菜单
        children = await self.system_repo.list_menus(parent_id=menu_id)
        if children:
            raise ValueError("该菜单下存在子菜单，无法删除")

        # 检查是否被角色使用
        from src.infrastructure.persistence.models.system_models import SystemUserRoleMenu

        count = await SystemUserRoleMenu.objects.filter(menu_id=menu_id).acount()
        if count > 0:
            raise ValueError("该菜单已被角色使用，无法删除")

        return await self.system_repo.delete_menu(menu_id)

    async def list_menus(self, is_active: bool | None = None) -> list[MenuResponseDTO]:
        """获取菜单列表"""
        menus = await self.system_repo.list_menus(is_active)
        return [await self._to_menu_response(menu) for menu in menus]

    async def get_menu_tree(self) -> list[MenuTreeDTO]:
        """获取菜单树形结构"""
        menus = await self.system_repo.list_menus()
        return self._build_menu_tree(menus)

    def _build_menu_tree(self, menus: list, parent_id: str | None = None) -> list[MenuTreeDTO]:
        """构建菜单树"""
        tree = []
        for menu in menus:
            if menu.parent_id == parent_id:
                children = self._build_menu_tree(menus, menu.id)
                tree.append(
                    MenuTreeDTO(
                        id=menu.id,
                        name=menu.name,
                        menu_type=menu.menu_type,
                        path=menu.path,
                        component=menu.component,
                        rank=menu.rank,
                        is_active=menu.is_active,
                        parent_id=menu.parent_id,
                        meta=self._to_menu_meta_response(menu.meta),
                        children=children,
                    )
                )
        return tree

    async def _to_menu_response(self, menu) -> MenuResponseDTO:
        """转换菜单响应DTO"""
        return MenuResponseDTO(
            id=menu.id,
            name=menu.name,
            menu_type=menu.menu_type,
            path=menu.path,
            component=menu.component,
            rank=menu.rank,
            is_active=menu.is_active,
            method=menu.method,
            description=menu.description,
            parent_id=menu.parent_id,
            meta=self._to_menu_meta_response(menu.meta),
            created_time=menu.created_time,
            updated_time=menu.updated_time,
        )

    def _to_menu_meta_response(self, meta) -> dict:
        """转换菜单元数据响应"""
        from src.application.dto.system import MenuMetaResponseDTO

        return MenuMetaResponseDTO(
            id=meta.id,
            title=meta.title,
            icon=meta.icon,
            r_svg_name=meta.r_svg_name,
            is_show_menu=meta.is_show_menu,
            is_show_parent=meta.is_show_parent,
            is_keepalive=meta.is_keepalive,
            frame_url=meta.frame_url,
            frame_loading=meta.frame_loading,
            transition_enter=meta.transition_enter,
            transition_leave=meta.transition_leave,
            is_hidden_tag=meta.is_hidden_tag,
            fixed_tag=meta.fixed_tag,
            dynamic_level=meta.dynamic_level,
        )

    # ========== 角色管理 ==========

    async def create_role(self, dto: RoleCreateDTO, creator_id: int | None = None) -> RoleResponseDTO:
        """创建角色"""
        # 检查角色编码是否已存在
        existing = await self.system_repo.get_role_by_code(dto.code)
        if existing:
            raise ValueError(f"角色编码 {dto.code} 已存在")

        # 创建角色
        role = await self.system_repo.create_role(dto, creator_id)

        # 获取菜单数量
        menus = await self.system_repo.get_role_menus(role.id)
        return await self._to_role_response(role, len(menus))

    async def get_role(self, role_id: str) -> RoleResponseDTO | None:
        """获取角色详情"""
        role = await self.system_repo.get_role_by_id(role_id)
        if not role:
            return None

        # 获取菜单数量
        menus = await self.system_repo.get_role_menus(role_id)
        return await self._to_role_response(role, len(menus))

    async def update_role(self, role_id: str, dto: RoleUpdateDTO, modifier_id: int | None = None) -> RoleResponseDTO:
        """更新角色"""
        # 检查角色编码是否重复
        if dto.code:
            existing = await self.system_repo.get_role_by_code(dto.code)
            if existing and existing.id != role_id:
                raise ValueError(f"角色编码 {dto.code} 已存在")

        role = await self.system_repo.update_role(role_id, dto, modifier_id)
        if not role:
            raise ValueError("角色不存在")

        # 获取菜单数量
        menus = await self.system_repo.get_role_menus(role_id)
        return await self._to_role_response(role, len(menus))

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        # 检查是否有用户使用该角色
        from src.infrastructure.persistence.models.system_models import SystemUserInfoRoles

        count = await SystemUserInfoRoles.objects.filter(userrole_id=role_id).acount()
        if count > 0:
            raise ValueError("该角色已被用户使用，无法删除")

        return await self.system_repo.delete_role(role_id)

    async def list_roles(self, is_active: bool | None = None) -> list[RoleResponseDTO]:
        """获取角色列表"""
        roles = await self.system_repo.list_roles(is_active)
        result = []
        for role in roles:
            menus = await self.system_repo.get_role_menus(role.id)
            result.append(await self._to_role_response(role, len(menus)))
        return result

    async def assign_menus_to_role(self, role_id: str, dto: RoleAssignMenuDTO) -> bool:
        """为角色分配菜单权限"""
        # 检查角色是否存在
        role = await self.system_repo.get_role_by_id(role_id)
        if not role:
            raise ValueError("角色不存在")

        # 检查菜单是否存在
        menus = await self.system_repo.get_menus_by_ids(dto.menu_ids)
        if len(menus) != len(dto.menu_ids):
            raise ValueError("部分菜单不存在")

        return await self.system_repo.assign_menus_to_role(role_id, dto.menu_ids)

    async def get_role_menus(self, role_id: str) -> list[MenuResponseDTO]:
        """获取角色的菜单列表"""
        menus = await self.system_repo.get_role_menus(role_id)
        return [await self._to_menu_response(menu) for menu in menus]

    async def _to_role_response(self, role, menu_count: int = 0) -> RoleResponseDTO:
        """转换角色响应DTO"""
        return RoleResponseDTO(
            id=role.id,
            name=role.name,
            code=role.code,
            is_active=role.is_active,
            description=role.description,
            menu_count=menu_count,
            created_time=role.created_time,
            updated_time=role.updated_time,
        )

    # ========== 用户角色管理 ==========

    async def assign_roles_to_user(self, user_id: int, role_ids: list[str]) -> bool:
        """为用户分配角色"""
        # 检查用户是否存在
        from src.infrastructure.persistence.models.user_models import User

        try:
            await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            raise ValueError("用户不存在")

        # 检查角色是否存在
        for role_id in role_ids:
            role = await self.system_repo.get_role_by_id(role_id)
            if not role:
                raise ValueError(f"角色 {role_id} 不存在")

        return await self.system_repo.assign_roles_to_user(user_id, role_ids)

    async def get_user_roles(self, user_id: int) -> list[RoleResponseDTO]:
        """获取用户的角色列表"""
        roles = await self.system_repo.get_user_roles(user_id)
        result = []
        for role in roles:
            menus = await self.system_repo.get_role_menus(role.id)
            result.append(await self._to_role_response(role, len(menus)))
        return result

    async def get_user_menus(self, user_id: int) -> list[MenuResponseDTO]:
        """获取用户的菜单权限列表（多角色取交集）"""
        menus = await self.system_repo.get_user_menus(user_id)
        return [await self._to_menu_response(menu) for menu in menus]

    # ========== 操作日志管理 ==========

    async def list_operation_logs(self, filters: LogFilterDTO) -> tuple[list[LogResponseDTO], int]:
        """获取操作日志列表"""
        logs, total = await self.system_repo.list_operation_logs(filters)
        return [self._to_log_response(log) for log in logs], total

    async def get_operation_log(self, log_id: int) -> LogResponseDTO | None:
        """获取操作日志详情"""
        log = await self.system_repo.get_operation_log_by_id(log_id)
        if not log:
            return None
        return self._to_log_response(log)

    def _to_log_response(self, log) -> LogResponseDTO:
        """转换操作日志响应DTO"""
        return LogResponseDTO(
            id=log.id,
            module=log.module,
            path=log.path,
            method=log.method,
            body=log.body,
            ipaddress=log.ipaddress,
            browser=log.browser,
            system=log.system,
            response_code=log.response_code,
            response_result=log.response_result,
            status_code=log.status_code,
            description=log.description,
            creator_id=log.creator_id,
            creator_name=log.creator.username if log.creator else None,
            created_time=log.created_time,
        )
