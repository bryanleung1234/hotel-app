import subprocess, sys, os

err_log = open(r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\startup_err.log', 'w')

proc = subprocess.Popen(
    [r'C:\Users\bryan\.workbuddy\binaries\python\envs\hotel\Scripts\python.exe',
     r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.py'],
    cwd=r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

import time
time.sleep(5)

if proc.poll() is not None:
    # Process ended
    print("Process ended with code:", proc.poll(), file=err_log)
    print("Stderr:", proc.communicate()[0], file=err_log)
else:
    print("Server running OK (PID:", proc.pid, ")", file=err_log)

err_log.close()
