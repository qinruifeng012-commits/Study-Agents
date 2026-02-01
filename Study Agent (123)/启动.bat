@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo 未找到虚拟环境 .venv，请先运行 启动服务.bat 或 setup_and_run.ps1
    pause
    exit /b 1
)

echo 正在启动 Study Agent ...
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
pause
