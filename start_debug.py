# -*- coding: utf-8 -*-
# 调试启动服务器，捕获完整错误信息
import subprocess, sys, time, os

PYTHON = r'C:\Users\bryan\.workbuddy\binaries\python\versions\3.13.12\python.exe'
APP = r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.py'
LOG = r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.log'

env = os.environ.copy()
env['FLASK_ENV'] = 'development'
env['FLASK_DEBUG'] = '1'

with open(LOG, 'w', encoding='utf-8') as lf:
    proc = subprocess.Popen(
        [PYTHON, APP],
        stdout=lf, stderr=lf,
        cwd=r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app',
        env=env
    )
    print(f"Server PID: {proc.pid}, log: {LOG}")
    time.sleep(5)
    if proc.poll() is not None:
        print("Server CRASHED!")
        with open(LOG, encoding='utf-8', errors='replace') as f:
            print(f.read())
    else:
        print("Server running OK")
