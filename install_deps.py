import subprocess
import sys

result = subprocess.run(
    [r'C:\Users\bryan\.workbuddy\binaries\python\envs\hotel\Scripts\python.exe', '-m', 'pip', 'install', 'flask', 'PyJWT', 'openpyxl'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout[-500:] if result.stdout else "")
print("STDERR:", result.stderr[-500:] if result.stderr else "")
print("Return code:", result.returncode)
