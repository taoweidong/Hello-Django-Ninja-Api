"""
系统仓储实现
System Repository Implementation - 系统相关数据持久化实现
"""

from src.application.dto.system.dept_dto import DeptCreateDTO, DeptUpdateDTO
from src.application.dto.system.log_dto import LogFilterDTO
from src.application.dto.system.menu_dto import MenuCreateDTO, MenuUpdateDTO
from src.application.dto.system.role_dto import RoleCreateDTO, RoleUpdateDTO
from src.infrastructure.persistence.models.system_models import (
    SystemDeptInfo,
    SystemMenu,
    SystemMenuMeta,
    SystemOperationLog,
    SystemUserInfoRoles,
    SystemUserRole,
    SystemUserRoleMenu,
)
from src.infrastructure.persistence.models.user_models import User


class SystemRepository:
    """系统仓储类 - 处理部门、菜单、角色、日志等数据操作"""

    # ========== 部门操作 ==========

    async def create_dept(self, dto: DeptCreateDTO, creator_id: int | None = None) -> SystemDeptInfo:
        """创建部门"""
        dept = SystemDeptInfo(
            name=dto.name,
            code=dto.code,
            rank=dto.rank,
            auto_bind=dto.auto_bind,
            is_active=dto.is_active,
            description=dto.description,
            parent_id=dto.parent_id,
            dept_belong_id=dto.dept_belong_id,
            creator_id=creator_id,
        )
        await dept.asave()
        return dept

    async def get_dept_by_id(self, dept_id: str) -> SystemDeptInfo | None:
        """根据ID获取部门"""
        try:
            return await SystemDeptInfo.objects.aget(id=dept_id)
        except SystemDeptInfo.DoesNotExist:
            return None

    async def get_dept_by_code(self, code: str) -> SystemDeptInfo | None:
        """根据编码获取部门"""
        try:
            return await SystemDeptInfo.objects.aget(code=code)
        except SystemDeptInfo.DoesNotExist:
            return None

    async def update_dept(self, dept_id: str, dto: DeptUpdateDTO, modifier_id: int | None = None) -> SystemDeptInfo | None:
        """更新部门"""
        try:
            dept = await SystemDeptInfo.objects.aget(id=dept_id)
            update_fields = []

            if dto.name is not None:
                dept.name = dto.name
                update_fields.append("name")
            if dto.code is not None:
                dept.code = dto.code
                update_fields.append("code")
            if dto.rank is not None:
                dept.rank = dto.rank
                update_fields.append("rank")
            if dto.auto_bind is not None:
                dept.auto_bind = dto.auto_bind
                update_fields.append("auto_bind")
            if dto.is_active is not None:
                dept.is_active = dto.is_active
                update_fields.append("is_active")
            if dto.description is not None:
                dept.description = dto.description
                update_fields.append("description")
            if dto.parent_id is not None:
                dept.parent_id = dto.parent_id
                update_fields.append("parent_id")
            if dto.dept_belong_id is not None:
                dept.dept_belong_id = dto.dept_belong_id
                update_fields.append("dept_belong_id")

            dept.modifier_id = modifier_id
            update_fields.append("modifier_id")

            await dept.asave(update_fields=update_fields)
            return dept
        except SystemDeptInfo.DoesNotExist:
            return None

    async def delete_dept(self, dept_id: str) -> bool:
        """删除部门"""
        try:
            dept = await SystemDeptInfo.objects.aget(id=dept_id)
            await dept.adelete()
            return True
        except SystemDeptInfo.DoesNotExist:
            return False

    async def list_depts(self, is_active: bool | None = None, parent_id: str | None = None) -> list[SystemDeptInfo]:
        """获取部门列表"""
        queryset = SystemDeptInfo.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        return [dept async for dept in queryset.order_by("rank", "created_time")]

    async def get_dept_tree(self) -> list[SystemDeptInfo]:
        """获取部门树形结构"""
        return [dept async for dept in SystemDeptInfo.objects.filter(parent__isnull=True).order_by("rank")]

    # ========== 菜单操作 ==========

    async def create_menu(self, dto: MenuCreateDTO, creator_id: int | None = None) -> SystemMenu:
        """创建菜单"""
        # 创建元数据
        meta = SystemMenuMeta(
            title=dto.meta.title,
            icon=dto.meta.icon,
            r_svg_name=dto.meta.r_svg_name,
            is_show_menu=dto.meta.is_show_menu,
            is_show_parent=dto.meta.is_show_parent,
            is_keepalive=dto.meta.is_keepalive,
            frame_url=dto.meta.frame_url,
            frame_loading=dto.meta.frame_loading,
            transition_enter=dto.meta.transition_enter,
            transition_leave=dto.meta.transition_leave,
            is_hidden_tag=dto.meta.is_hidden_tag,
            fixed_tag=dto.meta.fixed_tag,
            dynamic_level=dto.meta.dynamic_level,
            description=dto.meta.description,
            creator_id=creator_id,
        )
        await meta.asave()

        # 创建菜单
        menu = SystemMenu(
            name=dto.name,
            menu_type=dto.menu_type,
            path=dto.path,
            component=dto.component,
            rank=dto.rank,
            is_active=dto.is_active,
            method=dto.method,
            description=dto.description,
            parent_id=dto.parent_id,
            meta=meta,
            creator_id=creator_id,
        )
        await menu.asave()
        return menu

    async def get_menu_by_id(self, menu_id: str) -> SystemMenu | None:
        """根据ID获取菜单"""
        try:
            return await SystemMenu.objects.select_related("meta", "parent").aget(id=menu_id)
        except SystemMenu.DoesNotExist:
            return None

    async def get_menu_by_name(self, name: str) -> SystemMenu | None:
        """根据名称获取菜单"""
        try:
            return await SystemMenu.objects.aget(name=name)
        except SystemMenu.DoesNotExist:
            return None

    async def update_menu(self, menu_id: str, dto: MenuUpdateDTO, modifier_id: int | None = None) -> SystemMenu | None:
        """更新菜单"""
        try:
            menu = await SystemMenu.objects.aget(id=menu_id)
            update_fields = []

            if dto.name is not None:
                menu.name = dto.name
                update_fields.append("name")
            if dto.menu_type is not None:
                menu.menu_type = dto.menu_type
                update_fields.append("menu_type")
            if dto.path is not None:
                menu.path = dto.path
                update_fields.append("path")
            if dto.component is not None:
                menu.component = dto.component
                update_fields.append("component")
            if dto.rank is not None:
                menu.rank = dto.rank
                update_fields.append("rank")
            if dto.is_active is not None:
                menu.is_active = dto.is_active
                update_fields.append("is_active")
            if dto.method is not None:
                menu.method = dto.method
                update_fields.append("method")
            if dto.description is not None:
                menu.description = dto.description
                update_fields.append("description")
            if dto.parent_id is not None:
                menu.parent_id = dto.parent_id
                update_fields.append("parent_id")

            menu.modifier_id = modifier_id
            update_fields.append("modifier_id")

            await menu.asave(update_fields=update_fields)
            return menu
        except SystemMenu.DoesNotExist:
            return None

    async def delete_menu(self, menu_id: str) -> bool:
        """删除菜单"""
        try:
            menu = await SystemMenu.objects.aget(id=menu_id)
            # 删除关联的元数据
            await menu.meta.adelete()
            await menu.adelete()
            return True
        except SystemMenu.DoesNotExist:
            return False

    async def list_menus(self, is_active: bool | None = None, parent_id: str | None = None) -> list[SystemMenu]:
        """获取菜单列表"""
        queryset = SystemMenu.objects.select_related("meta", "parent")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        return [menu async for menu in queryset.order_by("rank", "created_time")]

    async def get_menu_tree(self) -> list[SystemMenu]:
        """获取菜单树形结构"""
        return [menu async for menu in SystemMenu.objects.select_related("meta").filter(parent__isnull=True).order_by("rank")]

    async def get_menus_by_ids(self, menu_ids: list[str]) -> list[SystemMenu]:
        """根据ID列表获取菜单"""
        return [menu async for menu in SystemMenu.objects.filter(id__in=menu_ids).select_related("meta")]

    # ========== 角色操作 ==========

    async def create_role(self, dto: RoleCreateDTO, creator_id: int | None = None) -> SystemUserRole:
        """创建角色"""
        role = SystemUserRole(name=dto.name, code=dto.code, is_active=dto.is_active, description=dto.description, creator_id=creator_id)
        await role.asave()

        # 分配菜单权限
        if dto.menu_ids:
            await self.assign_menus_to_role(role.id, dto.menu_ids)

        return role

    async def get_role_by_id(self, role_id: str) -> SystemUserRole | None:
        """根据ID获取角色"""
        try:
            return await SystemUserRole.objects.aget(id=role_id)
        except SystemUserRole.DoesNotExist:
            return None

    async def get_role_by_code(self, code: str) -> SystemUserRole | None:
        """根据编码获取角色"""
        try:
            return await SystemUserRole.objects.aget(code=code)
        except SystemUserRole.DoesNotExist:
            return None

    async def update_role(self, role_id: str, dto: RoleUpdateDTO, modifier_id: int | None = None) -> SystemUserRole | None:
        """更新角色"""
        try:
            role = await SystemUserRole.objects.aget(id=role_id)
            update_fields = []

            if dto.name is not None:
                role.name = dto.name
                update_fields.append("name")
            if dto.code is not None:
                role.code = dto.code
                update_fields.append("code")
            if dto.is_active is not None:
                role.is_active = dto.is_active
                update_fields.append("is_active")
            if dto.description is not None:
                role.description = dto.description
                update_fields.append("description")

            role.modifier_id = modifier_id
            update_fields.append("modifier_id")

            await role.asave(update_fields=update_fields)
            return role
        except SystemUserRole.DoesNotExist:
            return None

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        try:
            role = await SystemUserRole.objects.aget(id=role_id)
            await role.adelete()
            return True
        except SystemUserRole.DoesNotExist:
            return False

    async def list_roles(self, is_active: bool | None = None) -> list[SystemUserRole]:
        """获取角色列表"""
        queryset = SystemUserRole.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return [role async for role in queryset.order_by("created_time")]

    async def assign_menus_to_role(self, role_id: str, menu_ids: list[str]) -> bool:
        """为角色分配菜单权限"""
        try:
            await SystemUserRole.objects.aget(id=role_id)
            # 删除旧的菜单关联
            await SystemUserRoleMenu.objects.filter(userrole_id=role_id).adelete()
            # 创建新的菜单关联
            menu_relations = [SystemUserRoleMenu(userrole_id=role_id, menu_id=menu_id) for menu_id in menu_ids]
            await SystemUserRoleMenu.objects.abulk_create(menu_relations)
            return True
        except SystemUserRole.DoesNotExist:
            return False

    async def get_role_menus(self, role_id: str) -> list[SystemMenu]:
        """获取角色的菜单列表"""
        menu_ids = [rm.menu_id async for rm in SystemUserRoleMenu.objects.filter(userrole_id=role_id).values_list("menu_id", flat=True)]
        return await self.get_menus_by_ids(list(menu_ids))

    # ========== 用户角色关联操作 ==========

    async def assign_roles_to_user(self, user_id: int, role_ids: list[str]) -> bool:
        """为用户分配角色"""
        try:
            await User.objects.aget(id=user_id)
            # 删除旧的角色关联
            await SystemUserInfoRoles.objects.filter(userinfo_id=user_id).adelete()
            # 创建新的角色关联
            role_relations = [SystemUserInfoRoles(userinfo_id=user_id, userrole_id=role_id) for role_id in role_ids]
            await SystemUserInfoRoles.objects.abulk_create(role_relations)
            return True
        except User.DoesNotExist:
            return False

    async def get_user_roles(self, user_id: int) -> list[SystemUserRole]:
        """获取用户的角色列表"""
        role_ids = [ur.userrole_id async for ur in SystemUserInfoRoles.objects.filter(userinfo_id=user_id).values_list("userrole_id", flat=True)]
        return [role async for role in SystemUserRole.objects.filter(id__in=role_ids)]

    async def get_user_menus(self, user_id: int) -> list[SystemMenu]:
        """
        获取用户的菜单权限列表（多角色取交集）
        权限即菜单，多角色之间取交集
        """
        # 获取用户所有角色
        roles = await self.get_user_roles(user_id)
        if not roles:
            return []

        # 获取每个角色的菜单ID集合
        menu_id_sets = []
        for role in roles:
            menu_ids = {rm.menu_id async for rm in SystemUserRoleMenu.objects.filter(userrole_id=role.id).values_list("menu_id", flat=True)}
            if menu_ids:
                menu_id_sets.append(menu_ids)

        if not menu_id_sets:
            return []

        # 多角色取交集
        final_menu_ids = menu_id_sets[0] if len(menu_id_sets) == 1 else set.intersection(*menu_id_sets)

        # 获取菜单详情
        return await self.get_menus_by_ids(list(final_menu_ids))

    # ========== 操作日志操作 ==========

    async def create_operation_log(
        self,
        user_id: int | None,
        module: str | None,
        path: str | None,
        method: str | None,
        body: str | None,
        ipaddress: str | None,
        browser: str | None,
        system: str | None,
        response_code: int | None,
        response_result: str | None,
        status_code: int | None,
        description: str | None = None,
    ) -> SystemOperationLog:
        """创建操作日志"""
        log = SystemOperationLog(
            creator_id=user_id,
            module=module,
            path=path,
            method=method,
            body=body,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            response_code=response_code,
            response_result=response_result,
            status_code=status_code,
            description=description,
        )
        await log.asave()
        return log

    async def list_operation_logs(self, filters: LogFilterDTO) -> tuple[list[SystemOperationLog], int]:
        """获取操作日志列表（分页）"""
        queryset = SystemOperationLog.objects.all()

        # 应用过滤条件
        if filters.module:
            queryset = queryset.filter(module__icontains=filters.module)
        if filters.method:
            queryset = queryset.filter(method=filters.method)
        if filters.creator_id:
            queryset = queryset.filter(creator_id=filters.creator_id)
        if filters.start_time:
            queryset = queryset.filter(created_time__gte=filters.start_time)
        if filters.end_time:
            queryset = queryset.filter(created_time__lte=filters.end_time)
        if filters.response_code:
            queryset = queryset.filter(response_code=filters.response_code)

        # 统计总数
        total = await queryset.acount()

        # 分页
        offset = (filters.page - 1) * filters.page_size
        logs = [log async for log in queryset.select_related("creator").order_by("-created_time")[offset : offset + filters.page_size]]

        return logs, total

    async def get_operation_log_by_id(self, log_id: int) -> SystemOperationLog | None:
        """根据ID获取操作日志"""
        try:
            return await SystemOperationLog.objects.select_related("creator").aget(id=log_id)
        except SystemOperationLog.DoesNotExist:
            return None
