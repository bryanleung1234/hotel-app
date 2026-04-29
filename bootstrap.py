# -*- coding: utf-8 -*-
import sys, os, subprocess

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# 使用 hotel venv 的 Python（含 openpyxl）
PYTHON = os.path.join(os.path.dirname(sys.executable), '..', 'envs', 'hotel', 'Scripts', 'python.exe')
if not os.path.exists(PYTHON):
    PYTHON = sys.executable  # fallback

print("[1/4] Check dependencies (Flask, PyJWT, openpyxl)...")
deps = ['flask', 'PyJWT', 'openpyxl']
missing = []
for dep in deps:
    try:
        __import__(dep.lower().replace('pyjwt', 'jwt').replace('openpyxl', 'openpyxl'))
    except ImportError:
        missing.append(dep)

if missing:
    print(f"[2/4] Installing missing: {', '.join(missing)}...")
    r = subprocess.run([PYTHON, '-m', 'pip', 'install'] + deps,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[FAIL] {r.stderr[-300:]}")
        sys.exit(1)
    print("[OK] Dependencies installed")
else:
    print("[OK] All dependencies present")

print("[3/4] Starting server...")
os.chdir(APP_DIR)
os.execv(PYTHON, [PYTHON, os.path.join(APP_DIR, 'server.py')])