"""
用户服务测试
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def user_service():
    """用户服务 fixture"""
    from src.application.services.user_service import UserService

    mock_user_repo = Mock()
    mock_rbac_repo = Mock()
    mock_cache = Mock()
    return UserService(
        user_repository=mock_user_repo, rbac_repository=mock_rbac_repo, cache=mock_cache
    )


@pytest.mark.unit
class TestUserService:
    """用户服务单元测试"""

    def test_get_user_by_id_success(self, user_service):
        """测试根据 ID 获取用户成功"""
        # 模拟数据
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user.phone = "13800138000"
        mock_user.is_active = True
        mock_user.is_staff = False
        mock_user.is_superuser = False
        mock_user.created_at = "2024-01-01T00:00:00Z"
        mock_user.updated_at = "2024-01-01T00:00:00Z"

        user_service.user_repository.get_by_id.return_value = mock_user

        # 执行
        result = user_service.get_user_by_id(1)

        # 断言
        assert result is not None
        assert result.id == 1
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        user_service.user_repository.get_by_id.assert_called_once_with(1)

    def test_get_user_by_id_not_found(self, user_service):
        """测试获取不存在的用户"""
        user_service.user_repository.get_by_id.return_value = None

        # 执行
        result = user_service.get_user_by_id(999)

        # 断言
        assert result is None
        user_service.user_repository.get_by_id.assert_called_once_with(999)

    def test_list_users_success(self, user_service):
        """测试获取用户列表成功"""
        mock_users = [Mock(id=i, username=f"user{i}") for i in range(3)]
        user_service.user_repository.get_all.return_value = mock_users

        # 执行
        result = user_service.list_users(page=1, page_size=10)

        # 断言
        assert len(result.items) == 3
        assert result.total == 3
        assert result.page == 1
        assert result.page_size == 10
        user_service.user_repository.get_all.assert_called_once()

    def test_update_user_success(self, user_service):
        """测试更新用户成功"""
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "olduser"
        mock_user.email = "old@example.com"

        user_service.user_repository.get_by_id.return_value = mock_user
        user_service.user_repository.update.return_value = True

        # 执行
        result = user_service.update_user(user_id=1, email="new@example.com", phone="13900139000")

        # 断言
        assert result is True
        user_service.user_repository.get_by_id.assert_called_once_with(1)
        assert user_service.user_repository.update.called

    def test_delete_user_success(self, user_service):
        """测试删除用户成功"""
        mock_user = Mock()
        mock_user.id = 1

        user_service.user_repository.get_by_id.return_value = mock_user
        user_service.user_repository.delete.return_value = True

        # 执行
        result = user_service.delete_user(1)

        # 断言
        assert result is True
        user_service.user_repository.get_by_id.assert_called_once_with(1)
        user_service.user_repository.delete.assert_called_once_with(1)
