param(
    [int]$StartupTimeoutSeconds = 40
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $repoRoot ".runtime"
$runId = Get-Date -Format "yyyyMMdd-HHmmss"
$miniAppOutLog = Join-Path $runtimeDir ("miniapp-{0}.out.log" -f $runId)
$miniAppErrLog = Join-Path $runtimeDir ("miniapp-{0}.err.log" -f $runId)
$tunnelLog = Join-Path $runtimeDir ("cloudflared-{0}.log" -f $runId)
$envPath = Join-Path $repoRoot ".env"
$npmPath = "C:\Program Files\nodejs\npm.cmd"
$cloudflaredPath = "C:\Program Files (x86)\cloudflared\cloudflared.exe"

New-Item -ItemType Directory -Force $runtimeDir | Out-Null

Write-Host "Starting Mini App dev server..."
$miniAppProcess = Start-Process powershell `
    -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "& '$npmPath' run dev:miniapp" `
    -WorkingDirectory $repoRoot `
    -RedirectStandardOutput $miniAppOutLog `
    -RedirectStandardError $miniAppErrLog `
    -PassThru

$deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
$localUrl = $null
while ((Get-Date) -lt $deadline) {
    if (Test-Path $miniAppOutLog) {
        $content = Get-Content -Raw $miniAppOutLog
        $content = [regex]::Replace($content, "\x1b\[[0-9;]*m", "")
        $match = [regex]::Match($content, "http://localhost:(\d+)/")
        if ($match.Success) {
            $localUrl = "http://127.0.0.1:{0}" -f $match.Groups[1].Value
            break
        }
    }
    Start-Sleep -Milliseconds 500
}

if (-not $localUrl) {
    throw "Mini App dev server did not start in time. Check $miniAppOutLog and $miniAppErrLog."
}

Write-Host "Mini App is running at $localUrl"
Write-Host "Starting public tunnel..."
$tunnelProcess = Start-Process $cloudflaredPath `
    -ArgumentList "tunnel", "--url", $localUrl, "--protocol", "http2", "--no-autoupdate", "--logfile", $tunnelLog `
    -WorkingDirectory $repoRoot `
    -PassThru

$deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
$publicUrl = $null
while ((Get-Date) -lt $deadline) {
    if (Test-Path $tunnelLog) {
        $content = Get-Content -Raw $tunnelLog
        $match = [regex]::Match($content, "https://[a-z0-9-]+\.trycloudflare\.com")
        if ($match.Success) {
            $publicUrl = $match.Value
            break
        }
    }
    Start-Sleep -Milliseconds 500
}

if (-not $publicUrl) {
    throw "Tunnel URL was not generated in time. Check $tunnelLog."
}

if (-not (Test-Path $envPath)) {
    throw ".env was not found at $envPath"
}

$envContent = Get-Content -Raw $envPath
if ($envContent -match "(?m)^MINIAPP_URL=.*$") {
    $envContent = [regex]::Replace($envContent, "(?m)^MINIAPP_URL=.*$", "MINIAPP_URL=$publicUrl")
} else {
    $envContent = $envContent.TrimEnd() + [Environment]::NewLine + "MINIAPP_URL=$publicUrl" + [Environment]::NewLine
}
Set-Content -Path $envPath -Value $envContent -Encoding utf8

Write-Host ""
Write-Host "Mini App is publicly available at:"
Write-Host $publicUrl
Write-Host ""
Write-Host "Processes:"
Write-Host ("  Mini App PID: {0}" -f $miniAppProcess.Id)
Write-Host ("  Tunnel PID:   {0}" -f $tunnelProcess.Id)
Write-Host ("  Mini App log: {0}" -f $miniAppOutLog)
Write-Host ("  Tunnel log:   {0}" -f $tunnelLog)
Write-Host ""
Write-Host "Next step:"
Write-Host "  python -m app.bot.sync_telegram_ui"
