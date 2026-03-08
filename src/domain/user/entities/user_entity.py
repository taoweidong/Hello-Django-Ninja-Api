"""
用户实体
User Entity - 领域驱动设计核心实体
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserEntity:
    """
    用户实体类
    严格按照DDD规范设计，包含业务逻辑验证
    """

    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    date_joined: datetime = field(default_factory=datetime.now)
    last_login: datetime | None = None
    avatar: str | None = None
    phone: str | None = None
    bio: str | None = None

    def __post_init__(self):
        if self.username:
            self._validate_username()
        if self.email:
            self._validate_email()

    def _validate_username(self) -> None:
        """用户名验证逻辑"""
        if not self.username or len(self.username) < 3:
            raise ValueError("用户名长度不能少于3位")
        if len(self.username) > 50:
            raise ValueError("用户名长度不能超过50位")

    def _validate_email(self) -> None:
        """邮箱验证逻辑"""
        if self.email and "@" not in self.email:
            raise ValueError("邮箱格式不正确")

    def update_profile(
        self,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        bio: str = None,
        avatar: str = None,
    ) -> None:
        """更新用户信息的业务逻辑"""
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if phone is not None:
            self.phone = phone
        if bio is not None:
            self.bio = bio
        if avatar is not None:
            self.avatar = avatar

    def activate(self) -> None:
        """激活用户"""
        self.is_active = True

    def deactivate(self) -> None:
        """停用用户"""
        self.is_active = False

    def grant_staff(self) -> None:
        """授予员工权限"""
        self.is_staff = True

    def revoke_staff(self) -> None:
        """撤销员工权限"""
        self.is_staff = False

    def grant_superuser(self) -> None:
        """授予超级管理员权限"""
        self.is_superuser = True

    def revoke_superuser(self) -> None:
        """撤销超级管理员权限"""
        self.is_superuser = False

    def update_last_login(self) -> None:
        """更新最后登录时间"""
        self.last_login = datetime.now()

    def get_full_name(self) -> str:
        """获取用户全名"""
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "avatar": self.avatar,
            "phone": self.phone,
            "bio": self.bio,
        }
