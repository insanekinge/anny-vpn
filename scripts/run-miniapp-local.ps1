$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
$distDir = Join-Path $repoRoot "apps\miniapp\compat"
$port = 4301

function Resolve-PythonPath {
    $candidates = @(
        "C:\Users\sokka\AppData\Local\Programs\Python\Python312\python.exe",
        (Join-Path $repoRoot ".venv\Scripts\python.exe")
    )

    foreach ($candidate in $candidates) {
        if (-not $candidate) {
            continue
        }

        try {
            if (Test-Path $candidate) {
                return $candidate
            }
        } catch {
            continue
        }
    }

    $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        return $pythonCommand.Source
    }

    throw "Python runtime was not found. Install Python 3.12 or recreate the virtual environment."
}

function Stop-PortListener([int]$Port) {
    $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $listeners) {
        return
    }

    $processIds = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($processId in $processIds) {
        if (-not $processId) {
            continue
        }

        try {
            $process = Get-Process -Id $processId -ErrorAction Stop
            Write-Host "Stopping stale process on port ${Port}: $($process.ProcessName) (PID $processId)"
            Stop-Process -Id $processId -Force -ErrorAction Stop
        } catch {
            Write-Warning "Failed to stop process $processId on port ${Port}: $($_.Exception.Message)"
        }
    }
}

if (-not (Test-Path $distDir)) {
    throw "Mini App compat directory not found: $distDir"
}

$pythonPath = Resolve-PythonPath
Stop-PortListener -Port $port

Write-Host "Mini App local preview:"
Write-Host "  URL: http://127.0.0.1:$port"
Write-Host "  Press Ctrl+C to stop"
Write-Host ""

& $pythonPath -m http.server $port --bind 127.0.0.1 --directory $distDir
