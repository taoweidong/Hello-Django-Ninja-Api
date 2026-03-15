"""
认证服务测试
"""

import pytest


@pytest.mark.django_db
class TestAuthService:
    """认证服务单元测试"""

    def setup_method(self):
        """测试方法设置"""
        from src.application.services.auth_service import AuthService

        self.auth_service = AuthService()

    @pytest.mark.asyncio
    async def test_login_success(self, user_data):
        """测试登录成功"""
        from django.contrib.auth import get_user_model

        from src.application.dto.user import UserLoginDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)
        user.is_active = True
        await user.asave()

        login_dto = UserLoginDTO(username=user_data["username"], password=user_data["password"])

        result = await self.auth_service.login(login_dto)
        assert result is not None
        assert result.access_token is not None
        assert result.refresh_token is not None

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, user_data):
        """测试密码错误登录"""
        from django.contrib.auth import get_user_model

        from src.application.dto.user import UserLoginDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)
        user.is_active = True
        await user.asave()

        login_dto = UserLoginDTO(username=user_data["username"], password="wrongpassword")

        try:
            result = await self.auth_service.login(login_dto)
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "用户名或密码错误" in str(e)

    @pytest.mark.asyncio
    async def test_login_user_not_found(self):
        """测试用户不存在登录"""
        from src.application.dto.user import UserLoginDTO

        login_dto = UserLoginDTO(username="nonexistent", password="anypassword")

        try:
            result = await self.auth_service.login(login_dto)
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "用户名或密码错误" in str(e)

    @pytest.mark.asyncio
    async def test_login_inactive_user(self, user_data):
        """测试非活跃用户登录"""
        from django.contrib.auth import get_user_model

        from src.application.dto.user import UserLoginDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)
        user.is_active = False
        await user.asave()

        login_dto = UserLoginDTO(username=user_data["username"], password=user_data["password"])

        try:
            result = await self.auth_service.login(login_dto)
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "用户已被停用" in str(e)

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, user_data):
        """测试刷新 Token 成功"""
        from django.contrib.auth import get_user_model

        from src.application.dto.auth import RefreshTokenDTO
        from src.application.dto.user import UserLoginDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)
        user.is_active = True
        await user.asave()

        login_dto = UserLoginDTO(username=user_data["username"], password=user_data["password"])
        login_result = await self.auth_service.login(login_dto)

        if login_result.refresh_token:
            refresh_dto = RefreshTokenDTO(refresh_token=login_result.refresh_token)
            result = await self.auth_service.refresh_access_token(refresh_dto)
            assert result is not None
            assert result.access_token is not None

    @pytest.mark.asyncio
    async def test_logout_success(self, user_data):
        """测试登出成功"""
        from django.contrib.auth import get_user_model

        from src.application.dto.user import UserLoginDTO

        User = get_user_model()
        user = await User.objects.acreate_user(**user_data)
        user.is_active = True
        await user.asave()

        login_dto = UserLoginDTO(username=user_data["username"], password=user_data["password"])
        login_result = await self.auth_service.login(login_dto)

        await self.auth_service.logout(login_result.access_token)
        # 登出成功不抛出异常即可
