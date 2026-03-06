<#
.SYNOPSIS
    DeepBindDTA 一键部署脚本

.DESCRIPTION
    自动完成以下步骤：
      1. 检测前置依赖（Python、Docker）
      2. 创建/修复 Python 虚拟环境并安装依赖
      3. 启动 MySQL Docker 容器
      4. （可选）导入 SQL 数据
      5. 启动 GUI 主程序

.PARAMETER SkipDocker
    跳过 Docker / MySQL 启动步骤（已有外部 MySQL 时使用）

.PARAMETER ImportSQL
    强制执行 SQL 导入（否则默认询问）

.PARAMETER SkipImportSQL
    强制跳过 SQL 导入

.PARAMETER PredOnly
    不启动 GUI，直接运行预测脚本 pred.py

.EXAMPLE
    .\deploy.ps1
    .\deploy.ps1 -SkipDocker
    .\deploy.ps1 -ImportSQL
    .\deploy.ps1 -PredOnly
#>

param(
    [switch]$SkipDocker,
    [switch]$ImportSQL,
    [switch]$SkipImportSQL,
    [switch]$PredOnly
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
function Write-Step([string]$msg) {
    Write-Host "`n━━━ $msg" -ForegroundColor Cyan
}

function Write-OK([string]$msg) {
    Write-Host "  ✔ $msg" -ForegroundColor Green
}

function Write-Warn([string]$msg) {
    Write-Host "  ⚠ $msg" -ForegroundColor Yellow
}

function Write-Fail([string]$msg) {
    Write-Host "  ✘ $msg" -ForegroundColor Red
}

function Assert-Exit([string]$msg) {
    if ($LASTEXITCODE -ne 0) {
        Write-Fail $msg
        exit 1
    }
}

# ─────────────────────────────────────────────
# 进度提示
# ─────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║     DeepBindDTA  一键部署             ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Magenta

# ─────────────────────────────────────────────
# 步骤 1：检测 Python
# ─────────────────────────────────────────────
Write-Step "步骤 1/4：检测 Python"

$venvPy = Join-Path $root '.venv\Scripts\python.exe'
$venvOK = $false
if (Test-Path $venvPy) {
    try {
        & $venvPy -c "import sys" *> $null
        if ($LASTEXITCODE -eq 0) { $venvOK = $true }
    } catch {}
}

if ($venvOK) {
    $ver = & $venvPy --version 2>&1
    Write-OK "已有可用虚拟环境：$ver"
} else {
    Write-Warn "虚拟环境不存在或已损坏，开始创建..."
    $setupScript = Join-Path $root 'scripts\setup_py39.ps1'
    if (-not (Test-Path $setupScript)) {
        Write-Fail "未找到 scripts\setup_py39.ps1，请手动创建 .venv"
        exit 1
    }
    & powershell -ExecutionPolicy Bypass -File $setupScript
    Assert-Exit "虚拟环境创建失败"
    Write-OK "虚拟环境创建成功"
}

# ─────────────────────────────────────────────
# 步骤 2：启动 MySQL Docker
# ─────────────────────────────────────────────
Write-Step "步骤 2/4：启动 MySQL（Docker）"

if ($SkipDocker) {
    Write-Warn "已跳过 Docker 启动（-SkipDocker）"
} else {
    # 检测 docker
    try {
        docker info *> $null
        if ($LASTEXITCODE -ne 0) { throw }
    } catch {
        Write-Fail "Docker 未运行或未安装，请先启动 Docker Desktop"
        Write-Warn "如使用外部 MySQL，可加 -SkipDocker 参数跳过此步骤"
        exit 1
    }

    Write-Host "  启动容器..." -ForegroundColor Gray
    docker compose up -d
    Assert-Exit "docker compose up -d 失败"
    Write-OK "MySQL 容器已启动"

    # 等待 MySQL 就绪（最多 60 秒）
    Write-Host "  等待 MySQL 就绪" -ForegroundColor Gray
    $deadline = (Get-Date).AddSeconds(60)
    $mysqlPwd = $env:MYSQL_ROOT_PASSWORD
    if (-not $mysqlPwd) { $mysqlPwd = '12345' }
    $ready = $false
    while ((Get-Date) -lt $deadline) {
        $ping = docker exec deepbinddta-mysql mysqladmin ping -h 127.0.0.1 -uroot "-p$mysqlPwd" --silent 2>&1
        if ($LASTEXITCODE -eq 0) { $ready = $true; break }
        Write-Host "    ..." -ForegroundColor DarkGray
        Start-Sleep -Seconds 3
    }
    if (-not $ready) {
        Write-Fail "等待 MySQL 超时（60s），请检查容器日志：docker logs deepbinddta-mysql"
        exit 1
    }
    Write-OK "MySQL 就绪"
}

# ─────────────────────────────────────────────
# 步骤 3：导入 SQL 数据（可选）
# ─────────────────────────────────────────────
Write-Step "步骤 3/4：数据库初始化"

$sqlFile = Join-Path $root 'data\drug_discovery_dump.sql'
$doImport = $false

if ($SkipImportSQL) {
    Write-Warn "已跳过 SQL 导入（-SkipImportSQL）"
} elseif ($ImportSQL) {
    $doImport = $true
} elseif (-not $SkipDocker -and (Test-Path $sqlFile)) {
    Write-Host "  检测到 SQL 数据文件，是否导入？（首次部署需要，耗时较长）" -ForegroundColor Yellow
    Write-Host "  文件大小：$([math]::Round((Get-Item $sqlFile).Length/1MB, 1)) MB" -ForegroundColor Gray
    $ans = Read-Host "  导入数据？[y/N]"
    if ($ans -match '^[Yy]') { $doImport = $true }
}

if ($doImport) {
    $importScript = Join-Path $root 'scripts\db_import_docker.ps1'
    if (-not (Test-Path $importScript)) {
        Write-Fail "未找到 scripts\db_import_docker.ps1"
        exit 1
    }
    Write-Host "  开始导入 SQL，请耐心等待..." -ForegroundColor Yellow
    & powershell -ExecutionPolicy Bypass -File $importScript
    Assert-Exit "SQL 导入失败"
    Write-OK "SQL 导入完成"
} else {
    if (-not $SkipDocker) {
        Write-OK "跳过 SQL 导入（如需导入请加 -ImportSQL 或重新运行）"
    }
}

# ─────────────────────────────────────────────
# 步骤 4：启动应用
# ─────────────────────────────────────────────
Write-Step "步骤 4/4：启动应用"

$mplConfigDir = Join-Path $root '.mplconfig'
New-Item -ItemType Directory -Force -Path $mplConfigDir | Out-Null
$env:MPLCONFIGDIR = $mplConfigDir

if ($PredOnly) {
    $targetScript = Join-Path $root 'pred.py'
    Write-OK "运行预测脚本：pred.py"
} else {
    $targetScript = Join-Path $root 'app.py'
    Write-OK "启动 GUI 主程序：app.py"
}

Write-Host ""
& $venvPy -u $targetScript
