@echo off
cd /d "%~dp0"
echo Starting server...
start /b python server.py
timeout /t 4 /nobreak >nul
python -c "import urllib.request; r = urllib.request.urlopen('http://localhost:3000/api/seed', data=b''); print(r.read().decode())"
echo Done! Server running at http://localhost:3000
pause
