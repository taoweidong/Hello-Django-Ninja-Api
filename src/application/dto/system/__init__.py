"""
系统DTO模块
System DTO Module
"""

from src.application.dto.system.dept_dto import (
    DeptCreateDTO,
    DeptResponseDTO,
    DeptTreeDTO,
    DeptUpdateDTO,
)
from src.application.dto.system.log_dto import (
    LogFilterDTO,
    LogResponseDTO,
)
from src.application.dto.system.menu_dto import (
    MenuCreateDTO,
    MenuMetaCreateDTO,
    MenuMetaResponseDTO,
    MenuResponseDTO,
    MenuTreeDTO,
    MenuUpdateDTO,
)
from src.application.dto.system.role_dto import (
    RoleAssignMenuDTO,
    RoleCreateDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
)

__all__ = [
    # 部门
    "DeptCreateDTO",
    "DeptUpdateDTO",
    "DeptResponseDTO",
    "DeptTreeDTO",
    # 菜单
    "MenuCreateDTO",
    "MenuUpdateDTO",
    "MenuResponseDTO",
    "MenuTreeDTO",
    "MenuMetaCreateDTO",
    "MenuMetaResponseDTO",
    # 角色
    "RoleCreateDTO",
    "RoleUpdateDTO",
    "RoleResponseDTO",
    "RoleAssignMenuDTO",
    # 日志
    "LogResponseDTO",
    "LogFilterDTO",
]
