@echo off
chcp 65001 >nul
echo === Study Agent 项目启动脚本 ===

REM 检查虚拟环境是否存在
if not exist .venv (
    echo 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境并安装依赖
echo 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 升级 pip
echo 升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt

REM 检查关键依赖
echo.
echo 检查已安装的关键依赖:
pip list | findstr /i "fastapi uvicorn httpx pydantic sqlalchemy"

echo.
echo === 依赖安装完成 ===
echo.
echo 启动服务（使用 python -m，不依赖 PATH）...
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

pause
