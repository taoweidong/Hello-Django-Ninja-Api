"""
用户档案实体
User Profile Entity - 用户扩展信息
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProfileEntity:
    """
    用户档案实体
    存储用户的扩展信息
    """

    profile_id: str = field(default="")
    user_id: str = ""
    gender: str | None = None
    birthday: datetime | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    website: str | None = None
    company: str | None = None
    occupation: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(
        self,
        gender: str = None,
        birthday: datetime = None,
        address: str = None,
        city: str = None,
        country: str = None,
        website: str = None,
        company: str = None,
        occupation: str = None,
    ) -> None:
        """更新档案信息"""
        if gender is not None:
            self.gender = gender
        if birthday is not None:
            self.birthday = birthday
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if country is not None:
            self.country = country
        if website is not None:
            self.website = website
        if company is not None:
            self.company = company
        if occupation is not None:
            self.occupation = occupation
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "gender": self.gender,
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "website": self.website,
            "company": self.company,
            "occupation": self.occupation,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
