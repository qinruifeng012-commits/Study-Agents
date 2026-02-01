# 直接使用虚拟环境里的 Python 启动，无需先 activate
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "未找到虚拟环境 .venv，请先运行: .\setup_and_run.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "正在启动 Study Agent ..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
