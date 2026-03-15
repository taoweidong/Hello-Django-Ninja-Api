"""
菜单DTO
Menu DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MenuMetaCreateDTO(BaseModel):
    """菜单元数据创建DTO"""

    title: str | None = Field(None, max_length=255, description="菜单标题")
    icon: str | None = Field(None, max_length=255, description="图标")
    r_svg_name: str | None = Field(None, max_length=255, description="SVG图标名称")
    is_show_menu: bool = Field(default=True, description="是否显示菜单")
    is_show_parent: bool = Field(default=False, description="是否显示父级")
    is_keepalive: bool = Field(default=True, description="是否缓存")
    frame_url: str | None = Field(None, max_length=255, description="iframe地址")
    frame_loading: bool = Field(default=False, description="iframe加载状态")
    transition_enter: str | None = Field(None, max_length=255, description="进入动画")
    transition_leave: str | None = Field(None, max_length=255, description="离开动画")
    is_hidden_tag: bool = Field(default=False, description="是否隐藏标签")
    fixed_tag: bool = Field(default=False, description="固定标签")
    dynamic_level: int = Field(default=0, ge=0, description="动态层级")
    description: str | None = Field(None, max_length=256, description="描述")

    class Config:
        json_schema_extra = {"example": {"title": "用户管理", "icon": "user", "is_show_menu": True, "is_keepalive": True}}


class MenuMetaResponseDTO(BaseModel):
    """菜单元数据响应DTO"""

    id: str = Field(..., description="元数据ID")
    title: str | None = Field(None, description="菜单标题")
    icon: str | None = Field(None, description="图标")
    r_svg_name: str | None = Field(None, description="SVG图标名称")
    is_show_menu: bool = Field(..., description="是否显示菜单")
    is_show_parent: bool = Field(..., description="是否显示父级")
    is_keepalive: bool = Field(..., description="是否缓存")
    frame_url: str | None = Field(None, description="iframe地址")
    frame_loading: bool = Field(..., description="iframe加载状态")
    transition_enter: str | None = Field(None, description="进入动画")
    transition_leave: str | None = Field(None, description="离开动画")
    is_hidden_tag: bool = Field(..., description="是否隐藏标签")
    fixed_tag: bool = Field(..., description="固定标签")
    dynamic_level: int = Field(..., description="动态层级")

    class Config:
        from_attributes = True


class MenuCreateDTO(BaseModel):
    """菜单创建DTO"""

    name: str = Field(..., min_length=1, max_length=128, description="菜单名称")
    menu_type: int = Field(..., ge=0, le=2, description="菜单类型：0-目录，1-菜单，2-按钮")
    path: str = Field(..., max_length=255, description="路由路径")
    component: str | None = Field(None, max_length=255, description="组件路径")
    rank: int = Field(default=0, ge=0, description="排序")
    is_active: bool = Field(default=True, description="是否激活")
    method: str | None = Field(None, max_length=10, description="请求方法")
    description: str | None = Field(None, max_length=256, description="描述")
    parent_id: str | None = Field(None, description="父级菜单ID")
    meta: MenuMetaCreateDTO = Field(..., description="菜单元数据")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "用户管理",
                "menu_type": 1,
                "path": "/system/user",
                "component": "system/user/index",
                "rank": 1,
                "is_active": True,
                "method": None,
                "description": "用户管理菜单",
                "parent_id": None,
                "meta": {"title": "用户管理", "icon": "user", "is_show_menu": True, "is_keepalive": True},
            }
        }


class MenuUpdateDTO(BaseModel):
    """菜单更新DTO"""

    name: str | None = Field(None, min_length=1, max_length=128, description="菜单名称")
    menu_type: int | None = Field(None, ge=0, le=2, description="菜单类型")
    path: str | None = Field(None, max_length=255, description="路由路径")
    component: str | None = Field(None, max_length=255, description="组件路径")
    rank: int | None = Field(None, ge=0, description="排序")
    is_active: bool | None = Field(None, description="是否激活")
    method: str | None = Field(None, max_length=10, description="请求方法")
    description: str | None = Field(None, max_length=256, description="描述")
    parent_id: str | None = Field(None, description="父级菜单ID")

    class Config:
        json_schema_extra = {"example": {"name": "用户管理（更新）", "rank": 2, "description": "用户管理菜单（更新）"}}


class MenuResponseDTO(BaseModel):
    """菜单响应DTO"""

    id: str = Field(..., description="菜单ID")
    name: str = Field(..., description="菜单名称")
    menu_type: int = Field(..., description="菜单类型")
    path: str = Field(..., description="路由路径")
    component: str | None = Field(None, description="组件路径")
    rank: int = Field(..., description="排序")
    is_active: bool = Field(..., description="是否激活")
    method: str | None = Field(None, description="请求方法")
    description: str | None = Field(None, description="描述")
    parent_id: str | None = Field(None, description="父级菜单ID")
    meta: MenuMetaResponseDTO = Field(..., description="菜单元数据")
    created_time: datetime = Field(..., description="创建时间")
    updated_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class MenuTreeDTO(BaseModel):
    """菜单树形结构DTO"""

    id: str = Field(..., description="菜单ID")
    name: str = Field(..., description="菜单名称")
    menu_type: int = Field(..., description="菜单类型")
    path: str = Field(..., description="路由路径")
    component: str | None = Field(None, description="组件路径")
    rank: int = Field(..., description="排序")
    is_active: bool = Field(..., description="是否激活")
    parent_id: str | None = Field(None, description="父级菜单ID")
    meta: MenuMetaResponseDTO = Field(..., description="菜单元数据")
    children: list["MenuTreeDTO"] = Field(default_factory=list, description="子菜单列表")

    class Config:
        from_attributes = True
