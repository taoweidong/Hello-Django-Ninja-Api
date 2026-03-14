"""
通用CRUD仓储基类
Generic CRUD Repository - 提供通用的CRUD操作和实体转换
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db import models

# 类型变量
M = TypeVar("M", bound=models.Model)  # Django模型类型
E = TypeVar("E")  # 实体类型


class EntityConverter(ABC, Generic[M, E]):
    """
    实体转换器基类
    定义模型与实体之间的转换接口
    """

    @abstractmethod
    def to_entity(self, model: M) -> E:
        """
        模型转换为实体

        参数:
            model: Django模型实例

        返回:
            实体对象
        """
        pass

    @abstractmethod
    def to_model(self, entity: E, model: M | None = None) -> M:
        """
        实体转换为模型

        参数:
            entity: 实体对象
            model: 已有的模型实例（可选，用于更新）

        返回:
            Django模型实例
        """
        pass


class CRUDRepository(Generic[M, E], ABC):
    """
    通用CRUD仓储基类
    提供标准的CRUD操作实现

    类型参数:
        M: Django模型类型
        E: 实体类型
    """

    def __init__(self, model_class: type[M], converter: EntityConverter[M, E]):
        """
        初始化仓储

        参数:
            model_class: Django模型类
            converter: 实体转换器
        """
        self._model_class = model_class
        self._converter = converter

    async def get_by_id(self, id: str) -> E | None:
        """
        根据ID获取实体

        参数:
            id: 实体ID

        返回:
            实体对象，不存在则返回None
        """
        try:
            model = await self._model_class.objects.aget(id=id)
            return self._converter.to_entity(model)
        except self._model_class.DoesNotExist:
            return None

    async def get_all(self) -> list[E]:
        """
        获取所有实体

        返回:
            实体列表
        """
        models = await self._model_class.objects.all().alist()
        return [self._converter.to_entity(model) for model in models]

    async def list_all(self, page: int = 1, page_size: int = 10) -> list[E]:
        """
        分页获取实体列表

        参数:
            page: 页码（从1开始）
            page_size: 每页数量

        返回:
            实体列表
        """
        offset = (page - 1) * page_size
        models = await self._model_class.objects.all()[offset : offset + page_size].alist()
        return [self._converter.to_entity(model) for model in models]

    async def save(self, entity: E) -> E:
        """
        保存实体

        参数:
            entity: 实体对象

        返回:
            保存后的实体
        """
        model = self._converter.to_model(entity)
        await model.asave()
        return entity

    async def update(self, entity: E, id: str = None) -> E:
        """
        更新实体

        参数:
            entity: 实体对象
            id: 实体ID（可选）

        返回:
            更新后的实体
        """
        # 如果提供了ID，先获取现有模型
        existing_model = None
        if id:
            try:
                existing_model = await self._model_class.objects.aget(id=id)
            except self._model_class.DoesNotExist:
                pass

        model = self._converter.to_model(entity, existing_model)
        await model.asave()
        return entity

    async def delete(self, id: str) -> bool:
        """
        删除实体

        参数:
            id: 实体ID

        返回:
            是否删除成功
        """
        try:
            model = await self._model_class.objects.aget(id=id)
            await model.adelete()
            return True
        except self._model_class.DoesNotExist:
            return False

    async def exists(self, id: str) -> bool:
        """
        检查实体是否存在

        参数:
            id: 实体ID

        返回:
            是否存在
        """
        return await self._model_class.objects.filter(id=id).aexists()

    async def count(self) -> int:
        """
        统计实体总数

        返回:
            实体总数
        """
        return await self._model_class.objects.acount()

    async def get_by_field(self, field_name: str, value: any) -> E | None:
        """
        根据字段值获取实体

        参数:
            field_name: 字段名
            value: 字段值

        返回:
            实体对象，不存在则返回None
        """
        try:
            filter_kwargs = {field_name: value}
            model = await self._model_class.objects.aget(**filter_kwargs)
            return self._converter.to_entity(model)
        except self._model_class.DoesNotExist:
            return None

    async def list_by_field(
        self, field_name: str, value: any, page: int = 1, page_size: int = 10
    ) -> list[E]:
        """
        根据字段值分页获取实体列表

        参数:
            field_name: 字段名
            value: 字段值
            page: 页码
            page_size: 每页数量

        返回:
            实体列表
        """
        offset = (page - 1) * page_size
        filter_kwargs = {field_name: value}
        models = await self._model_class.objects.filter(**filter_kwargs)[
            offset : offset + page_size
        ].alist()
        return [self._converter.to_entity(model) for model in models]

    async def exists_by_field(self, field_name: str, value: any) -> bool:
        """
        检查字段值是否存在

        参数:
            field_name: 字段名
            value: 字段值

        返回:
            是否存在
        """
        filter_kwargs = {field_name: value}
        return await self._model_class.objects.filter(**filter_kwargs).aexists()
