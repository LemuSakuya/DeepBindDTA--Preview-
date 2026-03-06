$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
$venvPy = Join-Path $root '.venv\Scripts\python.exe'
$script = Join-Path $root 'app.py'
if ($args.Count -gt 0 -and $args[0] -eq 'pred') {
  $script = Join-Path $root 'pred.py'
}

# Matplotlib 首次导入可能会构建字体缓存；将缓存目录固定到项目内，避免落到慢盘/权限问题路径。
$mplConfigDir = Join-Path $root '.mplconfig'
New-Item -ItemType Directory -Force -Path $mplConfigDir | Out-Null
$env:MPLCONFIGDIR = $mplConfigDir

if (-not (Test-Path $venvPy)) {
  Write-Host 'Virtual env not found: .venv\Scripts\python.exe' -ForegroundColor Red
  Write-Host 'Please run setup_py39.ps1 to create .venv and install dependencies.' -ForegroundColor Yellow
  exit 1
}

# Verify venv is not broken (common: base Python path moved/deleted)-=
try {
  & $venvPy -c "import sys" *> $null
} catch {
}
if ($LASTEXITCODE -ne 0) {
  Write-Host 'Virtual env exists but is broken (base Python missing).' -ForegroundColor Red
  Write-Host 'Fix: run setup_py39.ps1 to rebuild .venv.' -ForegroundColor Yellow
  exit 1
}

& $venvPy -u $script

