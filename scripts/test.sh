#!/bin/bash

# 测试脚本

echo "🧪 运行测试..."

# 激活虚拟环境
source .venv/bin/activate

# 运行所有测试
pytest -v --tb=short --cov=src --cov-report=html --cov-report=term-missing

echo "📊 测试报告已生成在 htmlcov/ 目录"
