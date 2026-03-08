"""
邮箱值对象
Email Value Object - 不可变的邮箱验证
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    邮箱值对象
    不可变对象，用于邮箱验证和标准化
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("邮箱不能为空")
        if not self._is_valid_format():
            raise ValueError("邮箱格式不正确")

    def _is_valid_format(self) -> bool:
        """验证邮箱格式"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, self.value))

    def get_domain(self) -> str:
        """获取邮箱域名"""
        return self.value.split("@")[1] if "@" in self.value else ""

    def normalize(self) -> str:
        """标准化邮箱地址（小写）"""
        return self.value.lower()

    def __str__(self) -> str:
        return self.value
