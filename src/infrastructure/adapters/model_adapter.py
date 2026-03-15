"""
模型适配器基类
Model Adapter Base - 提供统一的模型与实体转换
"""

import contextlib
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from django.db import models
from pydantic import BaseModel

# 类型变量
M = TypeVar("M", bound=models.Model)  # Django模型类型
E = TypeVar("E", bound=BaseModel)  # 实体类型（Pydantic模型）


class BaseModelAdapter(ABC, Generic[M, E]):
    """
    模型适配器基类
    提供模型与实体之间的转换逻辑

    类型参数:
        M: Django模型类型
        E: 实体类型（Pydantic模型）
    """

    def __init__(self, model_class: type[M], entity_class: type[E]):
        """
        初始化适配器

        参数:
            model_class: Django模型类
            entity_class: 实体类
        """
        self._model_class = model_class
        self._entity_class = entity_class

    @abstractmethod
    def get_field_mapping(self) -> dict[str, str]:
        """
        获取字段映射关系

        返回:
            字段映射字典 {entity_field: model_field}
            例如: {"user_id": "id", "username": "username"}
        """
        pass

    def to_entity(self, model: M) -> E:
        """
        模型转换为实体

        参数:
            model: Django模型实例

        返回:
            实体对象
        """
        field_mapping = self.get_field_mapping()
        data = {}

        for entity_field, model_field in field_mapping.items():
            value = getattr(model, model_field)

            # 处理外键关系
            if isinstance(value, models.Model):
                # 如果是外键，转换为字符串ID
                value = str(value.id) if hasattr(value, "id") else str(value)

            # 处理日期时间
            # Pydantic会自动处理datetime对象

            # 处理UUID
            if hasattr(value, "hex"):
                value = str(value)

            data[entity_field] = value

        return self._entity_class(**data)

    def to_model(self, entity: E, model: M | None = None) -> M:
        """
        实体转换为模型

        参数:
            entity: 实体对象
            model: 已有的模型实例（可选，用于更新）

        返回:
            Django模型实例
        """
        field_mapping = self.get_field_mapping()

        if model is None:
            model = self._model_class()

        for entity_field, model_field in field_mapping.items():
            # 获取实体字段值
            value = getattr(entity, entity_field, None)

            if value is not None:
                # 处理UUID字段
                if model_field == "id" and isinstance(value, str):
                    import uuid

                    with contextlib.suppress(ValueError):
                        value = uuid.UUID(value)

                setattr(model, model_field, value)

        return model

    def to_entity_dict(self, model: M) -> dict[str, Any]:
        """
        模型转换为实体字典

        参数:
            model: Django模型实例

        返回:
            实体数据字典
        """
        field_mapping = self.get_field_mapping()
        data = {}

        for entity_field, model_field in field_mapping.items():
            value = getattr(model, model_field)

            # 处理特殊类型
            if hasattr(value, "hex"):  # UUID
                value = str(value)

            data[entity_field] = value

        return data

    def to_model_dict(self, entity: E) -> dict[str, Any]:
        """
        实体转换为模型字典

        参数:
            entity: 实体对象

        返回:
            模型数据字典
        """
        field_mapping = self.get_field_mapping()
        data = {}

        for entity_field, model_field in field_mapping.items():
            value = getattr(entity, entity_field, None)

            if value is not None:
                # 处理UUID字段
                if model_field == "id" and isinstance(value, str):
                    import uuid

                    with contextlib.suppress(ValueError):
                        value = uuid.UUID(value)

                data[model_field] = value

        return data


class SimpleModelAdapter(BaseModelAdapter[M, E]):
    """
    简单模型适配器
    提供基于字段映射的自动转换

    使用示例:
        adapter = SimpleModelAdapter(
            model_class=User,
            entity_class=UserEntity,
            field_mapping={
                "user_id": "id",
                "username": "username",
                "email": "email",
            }
        )
    """

    def __init__(self, model_class: type[M], entity_class: type[E], field_mapping: dict[str, str]):
        """
        初始化简单模型适配器

        参数:
            model_class: Django模型类
            entity_class: 实体类
            field_mapping: 字段映射字典
        """
        super().__init__(model_class, entity_class)
        self._field_mapping = field_mapping

    def get_field_mapping(self) -> dict[str, str]:
        """获取字段映射关系"""
        return self._field_mapping
