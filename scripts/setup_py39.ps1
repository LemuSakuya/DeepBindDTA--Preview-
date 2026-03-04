<#
Python environment bootstrap (Windows PowerShell 5.1 friendly)

Goal:
- Create/rebuild .venv under repo root (prefers Python 3.9 if available)
- Install requirements.txt

Note:
- If .venv is broken (base Python moved/deleted), you may see:
    No Python at "...\python.exe"
    This script will rebuild .venv.
#>

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Setting up Python (.venv)..." -ForegroundColor Green

# Optional override: set an explicit Python executable path to build .venv
# Example (current session):
#   $env:VENV_PYTHON = 'E:\\Python313\\python313.exe'
# Example (persist for user):
#   setx VENV_PYTHON "E:\\Python313\\python313.exe"
$overridePython = $env:VENV_PYTHON
if ($overridePython) {
    $overridePython = $overridePython.Trim('"').Trim()
    if (Test-Path $overridePython) {
        $pythonExe = $overridePython
        $ver = & $pythonExe --version 2>&1
        Write-Host "Using VENV_PYTHON: $ver ($pythonExe)" -ForegroundColor Green
    } else {
        Write-Host "VENV_PYTHON is set but not found: $overridePython" -ForegroundColor Yellow
    }
}

function Get-Python39Executable {
    $candidates = @(
        @{ exe = 'py'; args = @('-3.9') },
        @{ exe = 'python3.9'; args = @() },
        @{ exe = 'python'; args = @() }
    )

    foreach ($cand in $candidates) {
        try {
            $ver = & $cand.exe @($cand.args) --version 2>&1
        } catch {
            continue
        }
        if ($ver -notmatch 'Python 3\.9') {
            continue
        }
        try {
            $exePath = & $cand.exe @($cand.args) -c "import sys; print(sys.executable)" 2>$null
            $exePath = ($exePath | Select-Object -First 1)
            if ($exePath) {
                $exePath = $exePath.Trim()
            }
            if ($exePath -and (Test-Path $exePath)) {
                Write-Host "Found Python 3.9: $ver ($exePath)" -ForegroundColor Green
                return $exePath
            }
        } catch {
            continue
        }
    }

    return $null
}

$usedFallback = $false

if (-not $pythonExe) {
    $pythonExe = Get-Python39Executable
}

if (-not $pythonExe) {
    # Fallback: try known absolute paths on this machine
    $fallbacks = @(
        'E:\\Aconda\\python.exe',
        'E:\\Python313\\python313.exe'
    )
    foreach ($p in $fallbacks) {
        if (Test-Path $p) {
            $pythonExe = $p
            $usedFallback = $true
            break
        }
    }
}
if (-not $pythonExe) {
    Write-Host "Python 3.9 not found (py -3.9 / python3.9 / python)." -ForegroundColor Red
    Write-Host "Download: https://www.python.org/downloads/release/python-3913/" -ForegroundColor Yellow
    Write-Host "Or set VENV_PYTHON to an existing python.exe path to build .venv." -ForegroundColor Yellow
    exit 1
}

if ($usedFallback) {
    $ver = & $pythonExe --version 2>&1
    Write-Host "WARNING: Python 3.9 not found; using fallback interpreter: $ver ($pythonExe)" -ForegroundColor Yellow
    Write-Host "Some packages (e.g., RDKit) may require Python 3.9 + conda-forge." -ForegroundColor Yellow
}

$venvPy = Join-Path $root '.venv\Scripts\python.exe'

# 判断现有 .venv 是否可用，不可用则删除重建
$needRebuild = $true
if (Test-Path .\.venv\Scripts\python.exe) {
    try {
        & .\.venv\Scripts\python.exe -c "import sys" *> $null
        if ($LASTEXITCODE -eq 0) {
            $needRebuild = $false
            Write-Host "Existing .venv looks OK; reusing it." -ForegroundColor Green
        }
    } catch {
    }
}

if ($needRebuild) {
    if (Test-Path .\.venv) {
        Write-Host "Existing .venv is broken/incomplete; rebuilding." -ForegroundColor Yellow
        try { Remove-Item -Recurse -Force .\.venv } catch { }
    }
    Write-Host "`nCreating virtual environment: .venv" -ForegroundColor Yellow
    & $pythonExe -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# 激活虚拟环境
Write-Host "`nActivating .venv..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 升级 pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
& $venvPy -m pip install --upgrade pip setuptools wheel

# 安装依赖
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
& $venvPy -m pip install -r requirements.txt

# 提示安装 RDKit
Write-Host "`nRDKit note (optional):" -ForegroundColor Yellow
Write-Host "  conda install -c conda-forge rdkit" -ForegroundColor Cyan
Write-Host "  or" -ForegroundColor Yellow
Write-Host "  pip install rdkit" -ForegroundColor Cyan

Write-Host "`nDone." -ForegroundColor Green
Write-Host "`nActivate later:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White

