"""
RBAC仓储实现
RBAC Repository Implementation - 角色和权限数据持久化实现
"""

import uuid

from src.domain.rbac.entities.permission_entity import PermissionEntity
from src.domain.rbac.entities.role_entity import RoleEntity
from src.domain.rbac.repositories.rbac_repository import RBACRepositoryInterface
from src.infrastructure.persistence.models.rbac_models import Permission, Role, UserRole
from src.infrastructure.persistence.models.user_models import User


class RBACRepositoryImpl(RBACRepositoryInterface):
    """
    RBAC仓储实现
    负责角色和权限数据的数据库操作
    """

    # ========== 角色操作 ==========

    async def _role_to_entity(self, role_model: Role) -> RoleEntity:
        """角色模型转换为实体"""
        permissions = [p async for p in role_model.permissions.values_list("code", flat=True)]
        return RoleEntity(
            role_id=str(role_model.id),
            name=role_model.name,
            code=role_model.code,
            description=role_model.description or "",
            permissions=permissions,
            is_system=role_model.is_system,
            is_active=role_model.is_active,
            created_at=role_model.created_at,
            updated_at=role_model.updated_at,
            created_by=str(role_model.created_by_id) if role_model.created_by_id else None,
        )

    def _role_to_model(self, entity: RoleEntity) -> Role:
        """角色实体转换为模型"""
        return Role(
            id=uuid.UUID(entity.role_id) if entity.role_id else uuid.uuid4(),
            name=entity.name,
            code=entity.code,
            description=entity.description,
            is_system=entity.is_system,
            is_active=entity.is_active,
        )

    async def get_role_by_id(self, role_id: str) -> RoleEntity | None:
        """根据ID获取角色"""
        try:
            role = await Role.objects.aget(id=role_id)
            return await self._role_to_entity(role)
        except Role.DoesNotExist:
            return None

    async def get_role_by_code(self, code: str) -> RoleEntity | None:
        """根据角色代码获取角色"""
        try:
            role = await Role.objects.aget(code=code)
            return await self._role_to_entity(role)
        except Role.DoesNotExist:
            return None

    async def save_role(self, role: RoleEntity) -> RoleEntity:
        """保存角色"""
        role_model = self._role_to_model(role)
        await role_model.asave()

        # 保存权限关联
        if role.permissions:
            perms = [p async for p in Permission.objects.filter(code__in=role.permissions)]
            await role_model.permissions.aset(perms)

        return role

    async def update_role(self, role: RoleEntity) -> RoleEntity:
        """更新角色"""
        role_model = self._role_to_model(role)
        await role_model.asave()

        # 更新权限关联
        if role.permissions:
            perms = [p async for p in Permission.objects.filter(code__in=role.permissions)]
            await role_model.permissions.aset(perms)

        return role

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        try:
            role = await Role.objects.aget(id=role_id)
            await role.adelete()
            return True
        except Role.DoesNotExist:
            return False

    async def list_roles(self, is_active: bool = None) -> list[RoleEntity]:
        """获取角色列表"""
        queryset = Role.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        roles = [role async for role in queryset]
        return [await self._role_to_entity(role) for role in roles]

    # ========== 权限操作 ==========

    def _permission_to_entity(self, perm_model: Permission) -> PermissionEntity:
        """权限模型转换为实体"""
        return PermissionEntity(
            permission_id=str(perm_model.id),
            name=perm_model.name,
            code=perm_model.code,
            resource=perm_model.resource,
            action=perm_model.action,
            description=perm_model.description or "",
            is_active=perm_model.is_active,
            created_at=perm_model.created_at,
            updated_at=perm_model.updated_at,
        )

    def _permission_to_model(self, entity: PermissionEntity) -> Permission:
        """权限实体转换为模型"""
        return Permission(
            id=uuid.UUID(entity.permission_id) if entity.permission_id else uuid.uuid4(),
            name=entity.name,
            code=entity.code,
            resource=entity.resource,
            action=entity.action,
            description=entity.description,
            is_active=entity.is_active,
        )

    async def get_permission_by_id(self, permission_id: str) -> PermissionEntity | None:
        """根据ID获取权限"""
        try:
            perm = await Permission.objects.aget(id=permission_id)
            return self._permission_to_entity(perm)
        except Permission.DoesNotExist:
            return None

    async def get_permission_by_code(self, code: str) -> PermissionEntity | None:
        """根据权限代码获取权限"""
        try:
            perm = await Permission.objects.aget(code=code)
            return self._permission_to_entity(perm)
        except Permission.DoesNotExist:
            return None

    async def save_permission(self, permission: PermissionEntity) -> PermissionEntity:
        """保存权限"""
        perm_model = self._permission_to_model(permission)
        await perm_model.asave()
        return permission

    async def update_permission(self, permission: PermissionEntity) -> PermissionEntity:
        """更新权限"""
        perm_model = self._permission_to_model(permission)
        await perm_model.asave()
        return permission

    async def delete_permission(self, permission_id: str) -> bool:
        """删除权限"""
        try:
            perm = await Permission.objects.aget(id=permission_id)
            await perm.adelete()
            return True
        except Permission.DoesNotExist:
            return False

    async def list_permissions(
        self, is_active: bool = None, resource: str = None
    ) -> list[PermissionEntity]:
        """获取权限列表"""
        queryset = Permission.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if resource:
            queryset = queryset.filter(resource=resource)
        perms = [perm async for perm in queryset]
        return [self._permission_to_entity(perm) for perm in perms]

    # ========== 用户角色关联 ==========

    async def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """分配角色给用户"""
        try:
            user = await User.objects.aget(id=user_id)
            role = await Role.objects.aget(id=role_id)
            await UserRole.objects.acreate(user=user, role=role)
            return True
        except (User.DoesNotExist, Role.DoesNotExist):
            return False

    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        deleted_count, _ = await UserRole.objects.filter(user_id=user_id, role_id=role_id).adelete()
        return deleted_count > 0

    async def get_user_roles(self, user_id: str) -> list[RoleEntity]:
        """获取用户的所有角色"""
        user_roles = [ur async for ur in UserRole.objects.filter(user_id=user_id).select_related("role")]
        return [await self._role_to_entity(ur.role) for ur in user_roles]

    async def get_user_permissions(self, user_id: str) -> list[PermissionEntity]:
        """获取用户的所有权限"""
        user_roles = [
            ur async for ur in UserRole.objects.filter(user_id=user_id)
            .select_related("role")
            .prefetch_related("role__permissions")
        ]

        all_permissions = set()
        for ur in user_roles:
            role = ur.role
            perms = [p async for p in role.permissions.filter(is_active=True)]
            all_permissions.update([p.code for p in perms])

        # 获取权限实体
        perm_entities = []
        for code in all_permissions:
            perm = await self.get_permission_by_code(code)
            if perm:
                perm_entities.append(perm)

        return perm_entities

    async def has_permission(self, user_id: str, permission_code: str) -> bool:
        """检查用户是否拥有指定权限"""
        user_roles = [
            ur async for ur in UserRole.objects.filter(user_id=user_id)
            .select_related("role")
            .prefetch_related("role__permissions")
        ]

        for ur in user_roles:
            role = ur.role
            if not role.is_active:
                continue
            # 检查角色是否有权限
            has_perm = await role.permissions.filter(code=permission_code, is_active=True).aexists()
            if has_perm:
                return True

        return False


# 全局实例
rbac_repository = RBACRepositoryImpl()
