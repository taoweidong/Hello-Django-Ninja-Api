"""
RBAC服务
RBAC Service - 角色权限业务逻辑处理
"""

import uuid

from src.application.dto.rbac import AssignRoleDTO, PermissionResponseDTO, RoleCreateDTO, RoleResponseDTO, RoleUpdateDTO, UserRolesResponseDTO
from src.infrastructure.cache.cache_manager import cache_manager
from src.infrastructure.persistence.models.rbac_models import Permission, Role, UserRole
from src.infrastructure.persistence.models.user_models import User
from src.infrastructure.repositories.rbac_repo_impl import RBACRepositoryImpl


class RBACService:
    """
    RBAC应用服务
    处理角色和权限相关业务逻辑
    """

    def __init__(self):
        self.rbac_repo = RBACRepositoryImpl()

    # ========== 角色管理 ==========

    async def create_role(self, role_dto: RoleCreateDTO, _created_by: str = None) -> RoleResponseDTO:
        """创建角色"""
        # 检查角色代码是否存在
        existing = await self.rbac_repo.get_role_by_code(role_dto.code)
        if existing:
            raise ValueError(f"角色代码 {role_dto.code} 已存在")

        # 创建角色
        role = Role(id=uuid.uuid4(), name=role_dto.name, code=role_dto.code, description=role_dto.description)
        await role.asave()

        # 添加权限
        if role_dto.permissions:
            perms = [p async for p in Permission.objects.filter(code__in=role_dto.permissions)]
            await role.permissions.aset(perms)

        return await self._to_role_response(role)

    async def get_role(self, role_id: str) -> RoleResponseDTO | None:
        """获取角色"""
        role = await self.rbac_repo.get_role_by_id(role_id)
        if not role:
            return None
        return await self._to_role_response(role)

    async def get_role_by_code(self, code: str) -> RoleResponseDTO | None:
        """根据代码获取角色"""
        role = await self.rbac_repo.get_role_by_code(code)
        if not role:
            return None
        return await self._to_role_response(role)

    async def update_role(self, role_id: str, role_dto: RoleUpdateDTO) -> RoleResponseDTO:
        """更新角色"""
        role = await Role.objects.aget(id=role_id)
        if not role:
            raise ValueError("角色不存在")

        if role.is_system:
            raise ValueError("系统角色不可修改")

        # 更新字段
        if role_dto.name is not None:
            role.name = role_dto.name
        if role_dto.description is not None:
            role.description = role_dto.description

        await role.asave()

        # 更新权限
        if role_dto.permissions is not None:
            perms = [p async for p in Permission.objects.filter(code__in=role_dto.permissions)]
            await role.permissions.aset(perms)

        return await self._to_role_response(role)

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        role = await Role.objects.aget(id=role_id)
        if not role:
            raise ValueError("角色不存在")

        if role.is_system:
            raise ValueError("系统角色不可删除")

        await role.adelete()
        return True

    async def list_roles(self, is_active: bool = None) -> list[RoleResponseDTO]:
        """获取角色列表"""
        roles = await self.rbac_repo.list_roles(is_active)
        return [await self._to_role_response(role) for role in roles]

    # ========== 权限管理 ==========

    async def create_permission(self, name: str, code: str, description: str = "") -> PermissionResponseDTO:
        """创建权限"""
        # 检查权限代码是否存在
        existing = await self.rbac_repo.get_permission_by_code(code)
        if existing:
            raise ValueError(f"权限代码 {code} 已存在")

        resource, action = code.split(":") if ":" in code else (code, "")

        permission = Permission(id=uuid.uuid4(), name=name, code=code, resource=resource, action=action, description=description)
        await permission.asave()

        return self._to_permission_response(permission)

    async def get_permission(self, permission_id: str) -> PermissionResponseDTO | None:
        """获取权限"""
        permission = await self.rbac_repo.get_permission_by_id(permission_id)
        if not permission:
            return None
        return self._to_permission_response(permission)

    async def list_permissions(self, is_active: bool = None, resource: str = None) -> list[PermissionResponseDTO]:
        """获取权限列表"""
        permissions = await self.rbac_repo.list_permissions(is_active, resource)
        return [await self._to_permission_response(perm) for perm in permissions]

    async def initialize_system_permissions(self) -> list[PermissionResponseDTO]:
        """初始化系统权限"""
        from src.domain.rbac.entities.permission_entity import SYSTEM_PERMISSIONS

        created = []
        for perm_data in SYSTEM_PERMISSIONS:
            existing = await self.rbac_repo.get_permission_by_code(perm_data["code"])
            if not existing:
                await self.create_permission(name=perm_data["name"], code=perm_data["code"], description=perm_data.get("description", ""))
                created.append(perm_data["code"])

        return await self.list_permissions()

    # ========== 用户角色关联 ==========

    async def assign_role_to_user(self, assign_dto: AssignRoleDTO, assigned_by: str = None) -> bool:
        """分配角色给用户"""
        # 检查用户是否存在
        try:
            user = await User.objects.aget(id=assign_dto.user_id)
        except User.DoesNotExist:
            raise ValueError("用户不存在")

        # 检查角色是否存在
        role = await Role.objects.aget(id=assign_dto.role_id)
        if not role:
            raise ValueError("角色不存在")

        if not role.is_active:
            raise ValueError("角色已被停用")

        # 检查是否已分配
        exists = await UserRole.objects.filter(user_id=assign_dto.user_id, role_id=assign_dto.role_id).aexists()
        if exists:
            raise ValueError("用户已拥有此角色")

        # 分配角色
        await UserRole.objects.acreate(user=user, role=role, assigned_by_id=assigned_by)

        # 清除用户权限缓存
        cache_manager.delete_permissions_cache(assign_dto.user_id)
        cache_manager.delete_roles_cache(assign_dto.user_id)

        return True

    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        deleted_count, _ = await UserRole.objects.filter(user_id=user_id, role_id=role_id).adelete()

        if deleted_count > 0:
            # 清除用户权限缓存
            cache_manager.delete_permissions_cache(user_id)
            cache_manager.delete_roles_cache(user_id)
            return True

        return False

    async def get_user_roles(self, user_id: str) -> UserRolesResponseDTO:
        """获取用户的所有角色"""
        roles = await self.rbac_repo.get_user_roles(user_id)
        role_responses = [await self._to_role_response(role) for role in roles]

        permissions = await self.rbac_repo.get_user_permissions(user_id)
        permission_codes = [perm.code for perm in permissions]

        return UserRolesResponseDTO(user_id=user_id, roles=role_responses, permissions=permission_codes)

    async def check_user_permission(self, user_id: str, permission_code: str) -> bool:
        """检查用户是否拥有指定权限"""
        # 尝试从缓存获取
        cached_permissions = cache_manager.get_permissions_cache(user_id)
        if cached_permissions is not None:
            return permission_code in cached_permissions

        # 从数据库获取
        has_perm = await self.rbac_repo.has_permission(user_id, permission_code)

        # 缓存结果
        roles = await self.rbac_repo.get_user_roles(user_id)
        all_permissions = []
        for role in roles:
            all_permissions.extend(role.permissions)

        cache_manager.set_permissions_cache(user_id, list(set(all_permissions)))

        return has_perm

    # ========== 辅助方法 ==========

    async def _to_role_response(self, role) -> RoleResponseDTO:
        """转换为角色响应DTO - 支持Role模型和RoleEntity"""
        from src.domain.rbac.entities.role_entity import RoleEntity

        if isinstance(role, RoleEntity):
            # role是RoleEntity对象
            return RoleResponseDTO(
                role_id=role.role_id,
                name=role.name,
                code=role.code,
                description=role.description,
                permissions=role.permissions,
                is_system=role.is_system,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at,
            )
        else:
            # role是Role模型对象
            permissions = [p async for p in role.permissions.values_list("code", flat=True)]
            return RoleResponseDTO(
                role_id=str(role.id),
                name=role.name,
                code=role.code,
                description=role.description,
                permissions=permissions,
                is_system=role.is_system,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at,
            )

    async def _to_permission_response(self, permission) -> PermissionResponseDTO:
        """转换为权限响应DTO - 支持Permission模型和PermissionEntity"""
        from src.domain.rbac.entities.permission_entity import PermissionEntity

        if isinstance(permission, PermissionEntity):
            # permission是PermissionEntity对象
            return PermissionResponseDTO(
                permission_id=permission.permission_id,
                name=permission.name,
                code=permission.code,
                resource=permission.resource,
                action=permission.action,
                description=permission.description,
                is_active=permission.is_active,
                created_at=permission.created_at,
            )
        else:
            # permission是Permission模型对象
            return PermissionResponseDTO(
                permission_id=str(permission.id),
                name=permission.name,
                code=permission.code,
                resource=permission.resource,
                action=permission.action,
                description=permission.description,
                is_active=permission.is_active,
                created_at=permission.created_at,
            )


# 全局实例
rbac_service = RBACService()
