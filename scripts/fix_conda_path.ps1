<#
Fix conda PATH (Windows)

What it does:
- Detects a conda install root (defaults to E:\Aconda if present)
- Appends required conda directories to the *User* PATH if missing

Notes:
- This does NOT modify the Machine PATH.
- You must reopen PowerShell/Terminal for PATH changes to take effect.
#>

$ErrorActionPreference = 'Stop'

$condaRoot = $null
$preferred = 'E:\Aconda'
if (Test-Path $preferred) {
    $condaRoot = $preferred
}

if (-not $condaRoot) {
    Write-Host 'Conda root not found. Please edit this script and set $condaRoot to your Anaconda/Miniconda folder.' -ForegroundColor Red
    exit 1
}

$required = @(
    $condaRoot,
    (Join-Path $condaRoot 'condabin'),
    (Join-Path $condaRoot 'Scripts'),
    (Join-Path $condaRoot 'Library\bin')
)

$missing = @()
foreach ($p in $required) {
    if (-not (Test-Path $p)) {
        Write-Host "Warning: path does not exist: $p" -ForegroundColor Yellow
        continue
    }
    $missing += $p
}

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (-not $userPath) { $userPath = '' }

# Normalize for comparisons
$userEntries = $userPath -split ';' | Where-Object { $_ -and $_.Trim() } | ForEach-Object { $_.Trim() }

$toAdd = @()
foreach ($p in $missing) {
    if ($userEntries -notcontains $p) {
        $toAdd += $p
    }
}

if ($toAdd.Count -eq 0) {
    Write-Host 'User PATH already contains conda entries. No changes made.' -ForegroundColor Green
    exit 0
}

$newPath = ($toAdd + $userEntries) -join ';'
[Environment]::SetEnvironmentVariable('Path', $newPath, 'User')

Write-Host 'Updated User PATH (prepended conda paths):' -ForegroundColor Green
$toAdd | ForEach-Object { Write-Host "  + $_" -ForegroundColor Cyan }
Write-Host ''
Write-Host 'Next:' -ForegroundColor Yellow
Write-Host '  1) Close and reopen PowerShell/VS Code terminal' -ForegroundColor Yellow
Write-Host '  2) Run: conda --version' -ForegroundColor Yellow
