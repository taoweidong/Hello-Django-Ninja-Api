#!/bin/bash

# 开发环境初始化脚本

echo "🚀 开始设置开发环境..."

# 检查 UV 是否安装
if ! command -v uv &> /dev/null; then
    echo "📦 安装 UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 创建虚拟环境
echo "🐍 创建 Python 虚拟环境 (3.10.11)..."
uv venv --python 3.10.11

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "📚 安装项目依赖..."
uv pip install -e ".[dev]"

# 代码格式化
echo "✨ 代码格式化 (Ruff)..."
ruff format .

# 代码检查
echo "🔍 代码检查 (Ruff)..."
ruff check . --fix

# 类型检查
echo "📊 类型检查 (MyPy)..."
mypy src/

# 创建初始管理员账号（包含数据库迁移）
echo "👤 创建初始管理员账号..."
python scripts/init_admin.py

# 运行测试
echo "🧪 运行测试..."
pytest

echo "✅ 开发环境设置完成！"
echo "🎯 启动服务: python manage.py runserver"
