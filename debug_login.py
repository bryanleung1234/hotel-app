# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app')
os.chdir(r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app')

# patch server to run with debug
import importlib.util
spec = importlib.util.spec_from_file_location("server", r"C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\server.py")
m = importlib.util.module_from_spec(spec)

# Monkey-test the login logic directly
import sqlite3, jwt, datetime

JWT_SECRET = 'hotel-secret-key-2026'
DB_PATH = r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\hotel.db'

try:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    user = db.execute('SELECT * FROM users WHERE phone = ?', ('13802531098',)).fetchone()
    if user:
        print("User found:", dict(user))
        user_dict = dict(user)
        payload = {
            'id': user_dict['id'],
            'phone': user_dict['phone'],
            'role': user_dict['role'],
            'name': user_dict.get('name', ''),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        print("Token type:", type(token))
        print("Token:", token[:30] if token else "NONE")
        print("LOGIN OK")
    else:
        print("User NOT FOUND in DB")
        all_users = db.execute('SELECT phone, role FROM users').fetchall()
        print("All users:", [dict(u) for u in all_users])
except Exception as e:
    import traceback
    traceback.print_exc()
