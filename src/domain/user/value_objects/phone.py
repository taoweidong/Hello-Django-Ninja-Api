"""
电话值对象
Phone Value Object - 不可变的电话验证
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    """
    电话值对象
    不可变对象，用于电话验证和标准化
    支持国际格式
    """

    value: str
    country_code: str = "+86"  # 默认中国区号

    def __post_init__(self):
        if not self.value:
            raise ValueError("电话号码不能为空")
        # 移除空格和连字符
        self.value = re.sub(r"[\s-]", "", self.value)
        if not self._is_valid_format():
            raise ValueError("电话号码格式不正确")

    def _is_valid_format(self) -> bool:
        """验证电话格式"""
        # 中国手机号：1开头的11位数字
        pattern = r"^1[3-9]\d{9}$"
        return bool(re.match(pattern, self.value))

    def get_national_number(self) -> str:
        """获取国内号码（去掉国际区号）"""
        if self.value.startswith(self.country_code.lstrip("+")):
            return self.value[len(self.country_code.lstrip("+")) :]
        return self.value

    def format(self) -> str:
        """格式化显示"""
        num = self.get_national_number()
        if len(num) == 11:
            return f"{num[:3]}-{num[3:7]}-{num[7:]}"
        return self.value

    def __str__(self) -> str:
        return f"{self.country_code}{self.value}"
