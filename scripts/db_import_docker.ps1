<#
Import data/drug_discovery_dump.sql into the MySQL Docker container.

Assumptions (defaults match this repo's Python config):
- Container name: deepbinddta-mysql
- Root password: 12345 (override with $env:MYSQL_ROOT_PASSWORD)
- Database name: drug_discovery (override with $env:MYSQL_DATABASE)

This script avoids Windows stdin redirection pitfalls by copying the SQL file
into the container and importing it there.
#>

$ErrorActionPreference = 'Stop'

function Assert-LastExitCode([string] $message) {
    if ($LASTEXITCODE -ne 0) {
        throw "$message (exit code: $LASTEXITCODE)"
    }
}

$container = 'deepbinddta-mysql'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $scriptDir
Set-Location $root

$sqlFile = Join-Path $root 'data\drug_discovery_dump.sql'
if (-not (Test-Path $sqlFile)) {
    Write-Host "SQL file not found: $sqlFile" -ForegroundColor Red
    exit 1
}

$mysqlRootPassword = $env:MYSQL_ROOT_PASSWORD
if (-not $mysqlRootPassword) { $mysqlRootPassword = '12345' }

$dbName = $env:MYSQL_DATABASE
if (-not $dbName) { $dbName = 'drug_discovery' }

# Wait for MySQL to be reachable inside the container
Write-Host "Waiting for MySQL in container '$container'..." -ForegroundColor Yellow
$deadline = (Get-Date).AddMinutes(10)
while ($true) {
    $ok = $false
    try {
        docker exec $container mysqladmin --connect-timeout=2 ping -h 127.0.0.1 -uroot -p$mysqlRootPassword --silent *> $null
        if ($LASTEXITCODE -eq 0) { $ok = $true }
    } catch {
        $ok = $false
    }

    if ($ok) { break }
    if ((Get-Date) -gt $deadline) {
        throw "Timed out waiting for MySQL to be ready in container '$container'."
    }
    Start-Sleep -Seconds 3
}

Write-Host "Ensuring database exists: $dbName" -ForegroundColor Yellow
$createDb = "CREATE DATABASE IF NOT EXISTS $dbName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
docker exec -e "MYSQL_PWD=$mysqlRootPassword" $container mysql -uroot -e "$createDb"
Assert-LastExitCode "Failed to create/ensure database '$dbName'"

Write-Host "Importing SQL (this may take a while): $sqlFile" -ForegroundColor Yellow

$containerSqlPath = '/tmp/drug_discovery_dump.sql'
Write-Host "Copying SQL into container: $containerSqlPath" -ForegroundColor Yellow
docker cp "$sqlFile" "${container}:$containerSqlPath"
Assert-LastExitCode "Failed to copy SQL into container '$container'"

try {
    Write-Host "Running import inside container..." -ForegroundColor Yellow
    docker exec -e "MYSQL_PWD=$mysqlRootPassword" $container sh -lc "mysql -uroot $dbName < $containerSqlPath"
    Assert-LastExitCode "SQL import failed"
} finally {
    try {
        docker exec $container sh -lc "rm -f $containerSqlPath" *> $null
    } catch {
    }
}

Write-Host "Done importing SQL into $dbName" -ForegroundColor Green
