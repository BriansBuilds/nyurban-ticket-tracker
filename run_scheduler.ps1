# PowerShell script to run the availability checker every 3 minutes on Windows
# Run this script in the background or as a scheduled task

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptPath "check_availability.py"
$logFile = Join-Path $scriptPath "availability.log"

Write-Host "Starting NY Urban Ticket Tracker scheduler..."
Write-Host "Checking every 3 minutes to avoid throttling the server"
Write-Host "Press Ctrl+C to stop"

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] Running check..."
    
    try {
        python $pythonScript | Tee-Object -FilePath $logFile -Append
    }
    catch {
        Write-Host "[$timestamp] Error: $_" | Tee-Object -FilePath $logFile -Append
    }
    
    Start-Sleep -Seconds 180  # 3 minutes
}
