import sys, os

old_stderr = sys.stderr
sys.stderr = open(r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.log', 'w', encoding='utf-8', buffering=1)

sys.path.insert(0, r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app')
import server

sys.stderr.close()
sys.stderr = old_stderr