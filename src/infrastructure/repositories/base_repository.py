"""
基础仓储
Base Repository - 提供通用的仓储方法
"""

from typing import Generic, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T]):
    """
    基础仓储类
    提供常用的数据库操作方法
    """

    def __init__(self, model: type[T]):
        self.model = model

    def get_queryset(self):
        """获取查询集"""
        return self.model.objects.all()

    def get_active_queryset(self):
        """获取激活对象的查询集"""
        return self.model.objects.filter(is_active=True)

    async def get_by_id(self, id: str) -> T | None:
        """根据ID获取对象"""
        try:
            return await self.model.objects.aget(id=id)
        except self.model.DoesNotExist:
            return None

    async def get_by_field(self, field: str, value: any) -> T | None:
        """根据字段获取对象"""
        try:
            return await self.model.objects.aget(**{field: value})
        except self.model.DoesNotExist:
            return None

    async def save(self, obj: T) -> T:
        """保存对象"""
        await obj.asave()
        return obj

    async def create(self, **kwargs) -> T:
        """创建对象"""
        return await self.model.objects.acreate(**kwargs)

    async def update(self, obj: T, **kwargs) -> T:
        """更新对象"""
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await obj.asave()
        return obj

    async def delete(self, obj: T) -> bool:
        """删除对象"""
        await obj.adelete()
        return True

    async def list_all(self, page: int = 1, page_size: int = 10) -> list[T]:
        """获取列表"""
        offset = (page - 1) * page_size
        return list(await self.model.objects.all()[offset : offset + page_size])

    async def count(self) -> int:
        """获取总数"""
        return await self.model.objects.acount()

    async def exists(self, **kwargs) -> bool:
        """检查是否存在"""
        return await self.model.objects.filter(**kwargs).aexists()

    async def filter(self, page: int = 1, page_size: int = 10, **kwargs) -> list[T]:
        """过滤查询"""
        offset = (page - 1) * page_size
        return list(await self.model.objects.filter(**kwargs)[offset : offset + page_size])

    async def get_or_create(self, defaults: dict = None, **kwargs) -> tuple[T, bool]:
        """获取或创建"""
        return await self.model.objects.aget_or_create(defaults=defaults, **kwargs)

    async def update_or_create(self, defaults: dict = None, **kwargs) -> tuple[T, bool]:
        """更新或创建"""
        return await self.model.objects.aupdate_or_create(defaults=defaults, **kwargs)
