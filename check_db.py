import sqlite3
db = sqlite3.connect(r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\hotel.db')
tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)
for t in tables:
    cols = db.execute(f"PRAGMA table_info({t})").fetchall()
    print(f"\n{t}:", [c[1] for c in cols])
