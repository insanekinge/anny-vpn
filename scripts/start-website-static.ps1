$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $repoRoot ".runtime"
$distDir = Join-Path $repoRoot "apps\website\dist"
$npmPath = "C:\Program Files\nodejs\npm.cmd"
$pythonPath = Join-Path $repoRoot ".venv\Scripts\python.exe"
$port = 4300
$runId = Get-Date -Format "yyyyMMdd-HHmmss"
$serverOutLog = Join-Path $runtimeDir ("website-static-{0}.out.log" -f $runId)
$serverErrLog = Join-Path $runtimeDir ("website-static-{0}.err.log" -f $runId)

New-Item -ItemType Directory -Force $runtimeDir | Out-Null

Write-Host "Building website..."
& $npmPath run build:website

if (-not (Test-Path $distDir)) {
    throw "Website dist directory not found: $distDir"
}

Write-Host "Starting static server at http://127.0.0.1:$port ..."
$serverProcess = Start-Process powershell `
    -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "& '$pythonPath' -m http.server $port --bind 127.0.0.1 --directory '$distDir'" `
    -WorkingDirectory $repoRoot `
    -RedirectStandardOutput $serverOutLog `
    -RedirectStandardError $serverErrLog `
    -PassThru

Write-Host ""
Write-Host "Website static preview is running:"
Write-Host "  Local URL: http://127.0.0.1:$port"
Write-Host "  PID: $($serverProcess.Id)"
Write-Host "  Stdout: $serverOutLog"
Write-Host "  Stderr: $serverErrLog"
