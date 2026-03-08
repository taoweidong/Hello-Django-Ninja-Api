"""
部门DTO
Department DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class DeptCreateDTO(BaseModel):
    """部门创建DTO"""

    name: str = Field(..., min_length=1, max_length=128, description="部门名称")
    code: str = Field(..., min_length=1, max_length=128, description="部门编码")
    rank: int = Field(default=0, ge=0, description="排序")
    auto_bind: bool = Field(default=False, description="自动绑定")
    is_active: bool = Field(default=True, description="是否激活")
    description: str | None = Field(None, max_length=256, description="描述")
    parent_id: str | None = Field(None, description="上级部门ID")
    dept_belong_id: str | None = Field(None, description="归属部门ID")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "技术部",
                "code": "TECH_DEPT",
                "rank": 1,
                "auto_bind": False,
                "is_active": True,
                "description": "技术研发部门",
                "parent_id": None,
                "dept_belong_id": None,
            }
        }


class DeptUpdateDTO(BaseModel):
    """部门更新DTO"""

    name: str | None = Field(None, min_length=1, max_length=128, description="部门名称")
    code: str | None = Field(None, min_length=1, max_length=128, description="部门编码")
    rank: int | None = Field(None, ge=0, description="排序")
    auto_bind: bool | None = Field(None, description="自动绑定")
    is_active: bool | None = Field(None, description="是否激活")
    description: str | None = Field(None, max_length=256, description="描述")
    parent_id: str | None = Field(None, description="上级部门ID")
    dept_belong_id: str | None = Field(None, description="归属部门ID")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "技术部",
                "rank": 2,
                "description": "技术研发部门（更新）",
            }
        }


class DeptResponseDTO(BaseModel):
    """部门响应DTO"""

    id: str = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称")
    code: str = Field(..., description="部门编码")
    rank: int = Field(..., description="排序")
    auto_bind: bool = Field(..., description="自动绑定")
    is_active: bool = Field(..., description="是否激活")
    description: str | None = Field(None, description="描述")
    parent_id: str | None = Field(None, description="上级部门ID")
    parent_name: str | None = Field(None, description="上级部门名称")
    dept_belong_id: str | None = Field(None, description="归属部门ID")
    dept_belong_name: str | None = Field(None, description="归属部门名称")
    created_time: datetime = Field(..., description="创建时间")
    updated_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class DeptTreeDTO(BaseModel):
    """部门树形结构DTO"""

    id: str = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称")
    code: str = Field(..., description="部门编码")
    rank: int = Field(..., description="排序")
    is_active: bool = Field(..., description="是否激活")
    parent_id: str | None = Field(None, description="上级部门ID")
    children: list["DeptTreeDTO"] = Field(default_factory=list, description="子部门列表")

    class Config:
        from_attributes = True
