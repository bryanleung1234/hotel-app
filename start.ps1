$env:PYTHONIOENCODING = "utf-8"
$pythonExe = "C:\Users\bryan\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$projectDir = "C:\Users\bryan\WorkBuddy\20260426211044\hotel-app"

# Install flask
& $pythonExe -m pip install flask --quiet --user 2>&1 | Out-Null

# Seed data
Write-Host "📦 正在安装 Flask..."
$pipDone = $false
$job = Start-Job -ScriptBlock {
    param($py, $dir)
    & $py -m pip install flask --quiet --user 2>&1
} -ArgumentList $pythonExe, $projectDir

# Wait a bit then start server
Start-Sleep -Seconds 5
Stop-Job $job -ErrorAction SilentlyContinue
Remove-Job $job -ErrorAction SilentlyContinue

Write-Host "🚀 启动服务器..."
Set-Location $projectDir
& $pythonExe server.py
