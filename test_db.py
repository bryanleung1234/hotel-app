import sqlite3
db = sqlite3.connect(r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\hotel.db')
cur = db.cursor()
cur.execute("SELECT date, parking_tickets, parking_income, tax FROM daily_reports ORDER BY date DESC LIMIT 10")
rows = cur.fetchall()
print("日期,停车票数,停车收入,税费")
for r in rows:
    print(f"{r[0]},{r[1]},{r[2]},{r[3]}")
