#!/bin/bash

# 代码规范检查脚本

echo "🔍 代码规范检查..."

# 激活虚拟环境
source .venv/bin/activate

# Ruff 格式化检查
echo "📝 Ruff 格式化检查..."
ruff format --check .

# Ruff 代码检查
echo "🔎 Ruff 代码检查..."
ruff check .

# MyPy 类型检查
echo "📊 MyPy 类型检查..."
mypy src/

echo "✅ 代码规范检查完成！"
