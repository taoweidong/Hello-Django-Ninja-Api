"""
用户服务测试
"""

import pytest


@pytest.mark.django_db
class TestUserService:
    """用户服务单元测试"""

    def setup_method(self):
        """测试方法设置"""
        from src.application.services.user_service import UserService

        self.user_service = UserService()

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_data):
        """测试根据 ID 获取用户成功"""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)

        result = await self.user_service.get_user_by_id(str(user.id))
        assert result is not None
        assert result.username == user_data["username"]
        assert result.email == user_data["email"]

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self):
        """测试获取不存在的用户"""
        result = await self.user_service.get_user_by_id("99999")
        assert result is None

    @pytest.mark.asyncio
    async def test_list_users_success(self, user_data):
        """测试获取用户列表成功"""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        for i in range(3):
            data = user_data.copy()
            data["username"] = f"listuser{i}"
            data["email"] = f"listuser{i}@example.com"
            await User.objects.acreate_user(**data)

        result = await self.user_service.list_users(page=1, page_size=10)
        assert result is not None
        assert result.total >= 3

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_data):
        """测试更新用户成功"""
        from django.contrib.auth import get_user_model

        from src.application.dto.user import UserUpdateDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)

        update_dto = UserUpdateDTO(first_name="Updated", last_name="Name")
        result = await self.user_service.update_user(str(user.id), update_dto)
        assert result is not None
        assert result.first_name == "Updated"

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_data):
        """测试删除用户成功"""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)

        result = await self.user_service.delete_user(str(user.id))
        assert result is True
