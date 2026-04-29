import subprocess, os, time

# Kill old server
subprocess.run(['powershell', '-Command',
    'Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force'])
time.sleep(2)

# Start new server
srv_py = r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.py'
subprocess.Popen(
    [r'C:\Users\bryan\.workbuddy\binaries\python\versions\3.13.12\python.exe', srv_py],
    cwd=os.path.dirname(srv_py),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(4)
print("Server started OK")
