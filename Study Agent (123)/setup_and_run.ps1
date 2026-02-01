# Study Agent 项目启动脚本
# 用于激活虚拟环境、安装依赖并启动服务

Write-Host "=== Study Agent 项目启动脚本 ===" -ForegroundColor Cyan

# 检查虚拟环境是否存在
if (-not (Test-Path .venv)) {
    Write-Host "创建虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 检查是否成功激活
if ($LASTEXITCODE -ne 0) {
    Write-Host "虚拟环境激活失败，尝试使用 python -m venv 重新创建..." -ForegroundColor Red
    python -m venv .venv --clear
    & .\.venv\Scripts\Activate.ps1
}

# 清除可能阻止安装的环境变量
Write-Host "清除代理和 no-index 配置..." -ForegroundColor Yellow
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:PIP_NO_INDEX = ""

# 升级 pip
Write-Host "升级 pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖（使用国内镜像源）
Write-Host "安装项目依赖（使用清华镜像源）..." -ForegroundColor Yellow
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 检查关键依赖是否安装成功（避免管道符问题）
Write-Host "`n检查已安装的关键依赖:" -ForegroundColor Green
.\.venv\Scripts\python.exe -c "import subprocess; r=subprocess.run([r'.\.venv\Scripts\pip.exe','list'], capture_output=True, text=True); [print(line) for line in r.stdout.splitlines() if any(x in line.lower() for x in ['fastapi','uvicorn','httpx','pydantic','sqlalchemy'])]"

Write-Host "`n=== 依赖安装完成 ===" -ForegroundColor Green
Write-Host "`n启动服务请运行（无需激活虚拟环境）:" -ForegroundColor Cyan
Write-Host "  .\启动.ps1" -ForegroundColor White
Write-Host "  或: .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "`n或使用启动模式:" -ForegroundColor Cyan
Write-Host "  .\setup_and_run.ps1 -Run" -ForegroundColor White

# 如果传入了 -Run 参数，则直接启动服务（用 python -m 避免 PATH 问题）
if ($args -contains "-Run") {
    Write-Host "`n启动服务..." -ForegroundColor Yellow
    .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
}
