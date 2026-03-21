param(
    [switch]$Public,
    [ValidateSet("localtunnel", "cloudflared")]
    [string]$TunnelProvider = "localtunnel"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $repoRoot ".runtime"
$distDir = Join-Path $repoRoot "apps\miniapp\compat"
$npmPath = "C:\Program Files\nodejs\npm.cmd"
$pythonPath = Join-Path $repoRoot ".venv\Scripts\python.exe"
$cloudflaredPath = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$port = 4301
$envPath = Join-Path $repoRoot ".env"
$runId = Get-Date -Format "yyyyMMdd-HHmmss"
$serverOutLog = Join-Path $runtimeDir ("miniapp-static-{0}.out.log" -f $runId)
$serverErrLog = Join-Path $runtimeDir ("miniapp-static-{0}.err.log" -f $runId)
$tunnelLog = Join-Path $runtimeDir ("miniapp-static-tunnel-{0}.log" -f $runId)

New-Item -ItemType Directory -Force $runtimeDir | Out-Null

if (-not (Test-Path $distDir)) {
    throw "Mini App compat directory not found: $distDir"
}

Write-Host "Starting compatible Mini App server at http://127.0.0.1:$port ..."
$serverProcess = Start-Process powershell `
    -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "& '$pythonPath' -m http.server $port --bind 127.0.0.1 --directory '$distDir'" `
    -WorkingDirectory $repoRoot `
    -RedirectStandardOutput $serverOutLog `
    -RedirectStandardError $serverErrLog `
    -PassThru

Write-Host ""
Write-Host "Mini App static preview is running:"
Write-Host "  Local URL: http://127.0.0.1:$port"
Write-Host "  PID: $($serverProcess.Id)"
Write-Host "  Stdout: $serverOutLog"
Write-Host "  Stderr: $serverErrLog"

if (-not $Public) {
    return
}

Write-Host ""
Write-Host "Starting public tunnel..."

if ($TunnelProvider -eq "cloudflared") {
    $tunnelProcess = Start-Process $cloudflaredPath `
        -ArgumentList "tunnel", "--url", "http://127.0.0.1:$port", "--protocol", "http2", "--no-autoupdate", "--logfile", $tunnelLog `
        -WorkingDirectory $repoRoot `
        -PassThru
} else {
    $tunnelProcess = Start-Process powershell `
        -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "& 'C:\Program Files\nodejs\npx.cmd' localtunnel --port $port" `
        -WorkingDirectory $repoRoot `
        -RedirectStandardOutput $tunnelLog `
        -RedirectStandardError ($tunnelLog + ".err") `
        -PassThru
}

$deadline = (Get-Date).AddSeconds(40)
$publicUrl = $null
while ((Get-Date) -lt $deadline) {
    if (Test-Path $tunnelLog) {
        $content = Get-Content -Raw $tunnelLog
        if ($TunnelProvider -eq "cloudflared") {
            $match = [regex]::Match($content, "https://[a-z0-9-]+\.trycloudflare\.com")
        } else {
            $match = [regex]::Match($content, "https://[a-z0-9-]+\.loca\.lt")
        }
        if ($match.Success) {
            $publicUrl = $match.Value
            break
        }
    }
    Start-Sleep -Milliseconds 500
}

if (-not $publicUrl) {
    throw "Cloudflare tunnel URL was not generated. Check $tunnelLog"
}

$envContent = Get-Content -Raw $envPath
if ($envContent -match "(?m)^MINIAPP_URL=.*$") {
    $envContent = [regex]::Replace($envContent, "(?m)^MINIAPP_URL=.*$", "MINIAPP_URL=$publicUrl")
} else {
    $envContent = $envContent.TrimEnd() + [Environment]::NewLine + "MINIAPP_URL=$publicUrl" + [Environment]::NewLine
}
Set-Content -Path $envPath -Value $envContent -Encoding utf8

Write-Host ""
Write-Host "Public Mini App URL:"
Write-Host "  $publicUrl"
Write-Host "  Tunnel PID: $($tunnelProcess.Id)"
Write-Host "  Tunnel log: $tunnelLog"
Write-Host "  Provider: $TunnelProvider"
