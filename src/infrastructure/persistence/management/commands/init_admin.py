"""
Django管理命令：创建初始管理员账号
"""

import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """创建初始管理员账号"""

    help = "创建初始管理员账号"

    def handle(self, *args, **options):
        """执行命令"""
        from src.infrastructure.persistence.models.user_models import User

        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD", "admin123")

        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"用户 '{username}' 已存在，跳过创建"))
            return

        # 创建超级用户
        user = User.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS("初始管理员账号创建成功！"))
        self.stdout.write(f"  用户名: {username}")
        self.stdout.write(f"  邮箱: {email}")
        self.stdout.write(f"  密码: {password}")
        self.stdout.write(self.style.WARNING("\n⚠️  请在生产环境中修改默认密码！"))
