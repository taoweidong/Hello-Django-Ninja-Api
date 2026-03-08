"""
认证服务测试
"""

from unittest.mock import Mock

import pytest

from src.application.services.auth_service import AuthService


@pytest.fixture
def auth_service():
    """认证服务 fixture"""
    mock_user_repo = Mock()
    mock_jwt_manager = Mock()
    mock_cache = Mock()
    return AuthService(
        user_repository=mock_user_repo, jwt_manager=mock_jwt_manager, cache=mock_cache
    )


@pytest.mark.unit
class TestAuthService:
    """认证服务单元测试"""

    def test_login_success(self, auth_service):
        """测试登录成功"""
        # 模拟用户
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user.is_active = True
        mock_user.check_password.return_value = True

        auth_service.user_repository.get_by_username.return_value = mock_user

        # 模拟 JWT 生成
        auth_service.jwt_manager.generate_access_token.return_value = "access_token_123"
        auth_service.jwt_manager.generate_refresh_token.return_value = "refresh_token_123"

        # 执行
        result = auth_service.login(username="testuser", password="correctpassword")

        # 断言
        assert result is not None
        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_123"
        assert result.user_id == 1
        auth_service.user_repository.get_by_username.assert_called_once_with("testuser")

    def test_login_invalid_password(self, auth_service):
        """测试密码错误登录"""
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.check_password.return_value = False

        auth_service.user_repository.get_by_username.return_value = mock_user

        # 执行
        result = auth_service.login(username="testuser", password="wrongpassword")

        # 断言
        assert result is None

    def test_login_user_not_found(self, auth_service):
        """测试用户不存在登录"""
        auth_service.user_repository.get_by_username.return_value = None

        # 执行
        result = auth_service.login(username="nonexistent", password="anypassword")

        # 断言
        assert result is None
        auth_service.user_repository.get_by_username.assert_called_once_with("nonexistent")

    def test_login_inactive_user(self, auth_service):
        """测试非活跃用户登录"""
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.is_active = False
        mock_user.check_password.return_value = True

        auth_service.user_repository.get_by_username.return_value = mock_user

        # 执行
        result = auth_service.login(username="testuser", password="correctpassword")

        # 断言
        assert result is None

    def test_register_success(self, auth_service):
        """测试注册成功"""
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "newuser"

        auth_service.user_repository.create.return_value = mock_user

        # 执行
        result = auth_service.register(
            username="newuser", email="new@example.com", password="password123"
        )

        # 断言
        assert result is not None
        assert result.id == 1
        assert result.username == "newuser"
        auth_service.user_repository.create.assert_called_once()

    def test_refresh_token_success(self, auth_service):
        """测试刷新 Token 成功"""
        auth_service.jwt_manager.validate_refresh_token.return_value = Mock(user_id=1)
        mock_user = Mock()
        mock_user.id = 1
        auth_service.user_repository.get_by_id.return_value = mock_user
        auth_service.jwt_manager.generate_access_token.return_value = "new_access_token"

        # 执行
        result = auth_service.refresh_token("valid_refresh_token")

        # 断言
        assert result == "new_access_token"
        auth_service.jwt_manager.validate_refresh_token.assert_called_once_with(
            "valid_refresh_token"
        )

    def test_logout_success(self, auth_service):
        """测试登出成功"""
        auth_service.jwt_manager.decode_token.return_value = Mock(user_id=1)
        auth_service.cache.delete.return_value = True

        # 执行
        result = auth_service.logout("access_token")

        # 断言
        assert result is True
        auth_service.jwt_manager.decode_token.assert_called_once_with("access_token")
        auth_service.cache.delete.assert_called_once()
