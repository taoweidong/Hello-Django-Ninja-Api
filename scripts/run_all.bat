@echo off
echo ============================================================
echo 数据库迁移和API测试脚本
echo ============================================================

echo.
echo 步骤 1: 创建迁移文件...
python manage.py makemigrations
if %ERRORLEVEL% EQU 0 (
    echo [OK] makemigrations 完成
) else (
    echo [警告] makemigrations 可能已存在迁移
)

echo.
echo 步骤 2: 应用迁移...
python manage.py migrate --run-syncdb
if %ERRORLEVEL% EQU 0 (
    echo [OK] migrate 完成
) else (
    echo [错误] migrate 失败
    pause
    exit /b 1
)

echo.
echo 步骤 3: 创建管理员用户...
python scripts\init_admin.py
if %ERRORLEVEL% EQU 0 (
    echo [OK] 管理员创建完成
) else (
    echo [警告] 管理员可能已存在
)

echo.
echo 步骤 4: 启动服务...
start /B python manage.py runserver 8000
timeout /t 5 /nobreak >nul
echo [OK] 服务已启动

echo.
echo 步骤 5: 测试API...
python test_api.py

echo.
echo ============================================================
echo [完成] 所有步骤已完成!
echo ============================================================
echo.
echo 服务运行在: http://127.0.0.1:8000
echo API文档: http://127.0.0.1:8000/api/docs
echo.
pause
