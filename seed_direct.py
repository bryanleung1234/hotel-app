# -*- coding: utf-8 -*-
import sqlite3, os

DB = r'C:\Users\bryan\WorkBuddy\20260426211044\hotel-app\hotel.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

seed_data = [
    {'date':'2026-04-01','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':576,'ctrip_income':416,'fliggy_income':208,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':4,'parking_income':60,'tax':138,'total_rooms':25,'avg_price':148,'occupancy_rate':64.0,'revpgr':94.7,'total_income':3485},
    {'date':'2026-04-02','shift':'早班','meituan_rooms':4,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':5,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':990,'cash_income':416,'alipay_income':624,'parking_tickets':3,'parking_income':45,'tax':132,'total_rooms':25,'avg_price':145,'occupancy_rate':76.0,'revpgr':110.2,'total_income':3808},
    {'date':'2026-04-03','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':3,'alipay_rooms':4,'meituan_income':960,'ctrip_income':624,'fliggy_income':198,'douyin_income':396,'wechat_income':792,'cash_income':624,'alipay_income':828,'parking_tickets':5,'parking_income':75,'tax':156,'total_rooms':25,'avg_price':148,'occupancy_rate':88.0,'revpgr':130.2,'total_income':4422},
    {'date':'2026-04-04','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':5,'cash_rooms':3,'alipay_rooms':3,'meituan_income':960,'ctrip_income':624,'fliggy_income':396,'douyin_income':198,'wechat_income':990,'cash_income':624,'alipay_income':624,'parking_tickets':6,'parking_income':90,'tax':152,'total_rooms':25,'avg_price':145,'occupancy_rate':88.0,'revpgr':127.6,'total_income':4416},
    {'date':'2026-04-05','shift':'早班','meituan_rooms':4,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':5,'cash_rooms':3,'alipay_rooms':2,'meituan_income':768,'ctrip_income':624,'fliggy_income':396,'douyin_income':198,'wechat_income':990,'cash_income':624,'alipay_income':416,'parking_tickets':5,'parking_income':75,'tax':144,'total_rooms':25,'avg_price':145,'occupancy_rate':80.0,'revpgr':116.0,'total_income':4016},
    {'date':'2026-04-06','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':960,'ctrip_income':624,'fliggy_income':396,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':5,'parking_income':75,'tax':148,'total_rooms':25,'avg_price':146,'occupancy_rate':84.0,'revpgr':122.6,'total_income':4208},
    {'date':'2026-04-07','shift':'早班','meituan_rooms':5,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':5,'cash_rooms':2,'alipay_rooms':4,'meituan_income':960,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':990,'cash_income':416,'alipay_income':828,'parking_tickets':4,'parking_income':60,'tax':136,'total_rooms':25,'avg_price':148,'occupancy_rate':84.0,'revpgr':124.3,'total_income':4204},
    {'date':'2026-04-08','shift':'早班','meituan_rooms':4,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':2,'meituan_income':768,'ctrip_income':624,'fliggy_income':396,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':416,'parking_tickets':3,'parking_income':45,'tax':124,'total_rooms':25,'avg_price':145,'occupancy_rate':72.0,'revpgr':104.4,'total_income':3610},
    {'date':'2026-04-09','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':3,'cash_rooms':2,'alipay_rooms':2,'meituan_income':576,'ctrip_income':416,'fliggy_income':198,'douyin_income':198,'wechat_income':594,'cash_income':416,'alipay_income':416,'parking_tickets':3,'parking_income':45,'tax':116,'total_rooms':25,'avg_price':142,'occupancy_rate':56.0,'revpgr':79.5,'total_income':2814},
    {'date':'2026-04-10','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':2,'meituan_income':576,'ctrip_income':416,'fliggy_income':198,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':416,'parking_tickets':2,'parking_income':30,'tax':116,'total_rooms':25,'avg_price':145,'occupancy_rate':60.0,'revpgr':87.0,'total_income':3012},
    {'date':'2026-04-11','shift':'早班','meituan_rooms':4,'ctrip_rooms':2,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':2,'meituan_income':768,'ctrip_income':416,'fliggy_income':396,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':416,'parking_tickets':3,'parking_income':45,'tax':124,'total_rooms':25,'avg_price':145,'occupancy_rate':68.0,'revpgr':98.6,'total_income':3402},
    {'date':'2026-04-12','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':3,'cash_rooms':2,'alipay_rooms':2,'meituan_income':576,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':594,'cash_income':416,'alipay_income':416,'parking_tickets':3,'parking_income':45,'tax':118,'total_rooms':25,'avg_price':142,'occupancy_rate':60.0,'revpgr':85.2,'total_income':3012},
    {'date':'2026-04-13','shift':'早班','meituan_rooms':4,'ctrip_rooms':3,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':624,'fliggy_income':198,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':4,'parking_income':60,'tax':138,'total_rooms':25,'avg_price':145,'occupancy_rate':76.0,'revpgr':110.2,'total_income':3818},
    {'date':'2026-04-14','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':5,'cash_rooms':3,'alipay_rooms':3,'meituan_income':960,'ctrip_income':624,'fliggy_income':396,'douyin_income':198,'wechat_income':990,'cash_income':624,'alipay_income':624,'parking_tickets':6,'parking_income':90,'tax':152,'total_rooms':25,'avg_price':145,'occupancy_rate':88.0,'revpgr':127.6,'total_income':4416},
    {'date':'2026-04-15','shift':'早班','meituan_rooms':5,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':4,'meituan_income':960,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':828,'parking_tickets':5,'parking_income':75,'tax':144,'total_rooms':25,'avg_price':148,'occupancy_rate':80.0,'revpgr':118.4,'total_income':4006},
    {'date':'2026-04-16','shift':'早班','meituan_rooms':4,'ctrip_rooms':2,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':416,'fliggy_income':396,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':3,'parking_income':45,'tax':130,'total_rooms':25,'avg_price':145,'occupancy_rate':72.0,'revpgr':104.4,'total_income':3610},
    {'date':'2026-04-17','shift':'早班','meituan_rooms':4,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':2,'meituan_income':768,'ctrip_income':416,'fliggy_income':198,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':416,'parking_tickets':3,'parking_income':45,'tax':122,'total_rooms':25,'avg_price':145,'occupancy_rate':64.0,'revpgr':92.8,'total_income':3204},
    {'date':'2026-04-18','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':3,'cash_rooms':2,'alipay_rooms':2,'meituan_income':576,'ctrip_income':416,'fliggy_income':198,'douyin_income':198,'wechat_income':594,'cash_income':416,'alipay_income':416,'parking_tickets':2,'parking_income':30,'tax':112,'total_rooms':25,'avg_price':142,'occupancy_rate':56.0,'revpgr':79.5,'total_income':2814},
    {'date':'2026-04-19','shift':'早班','meituan_rooms':3,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':1,'meituan_income':576,'ctrip_income':416,'fliggy_income':198,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':208,'parking_tickets':2,'parking_income':30,'tax':108,'total_rooms':25,'avg_price':143,'occupancy_rate':56.0,'revpgr':80.1,'total_income':2804},
    {'date':'2026-04-20','shift':'早班','meituan_rooms':4,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':3,'parking_income':45,'tax':128,'total_rooms':25,'avg_price':145,'occupancy_rate':72.0,'revpgr':104.4,'total_income':3610},
    {'date':'2026-04-21','shift':'早班','meituan_rooms':4,'ctrip_rooms':3,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':5,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':624,'fliggy_income':198,'douyin_income':396,'wechat_income':990,'cash_income':416,'alipay_income':624,'parking_tickets':5,'parking_income':75,'tax':140,'total_rooms':25,'avg_price':145,'occupancy_rate':80.0,'revpgr':116.0,'total_income':4016},
    {'date':'2026-04-22','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':2,'wechat_rooms':5,'cash_rooms':3,'alipay_rooms':3,'meituan_income':960,'ctrip_income':624,'fliggy_income':396,'douyin_income':396,'wechat_income':990,'cash_income':624,'alipay_income':624,'parking_tickets':5,'parking_income':75,'tax':150,'total_rooms':25,'avg_price':145,'occupancy_rate':88.0,'revpgr':127.6,'total_income':4414},
    {'date':'2026-04-23','shift':'早班','meituan_rooms':5,'ctrip_rooms':2,'fliggy_rooms':1,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':4,'meituan_income':960,'ctrip_income':416,'fliggy_income':198,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':828,'parking_tickets':5,'parking_income':75,'tax':144,'total_rooms':25,'avg_price':148,'occupancy_rate':80.0,'revpgr':118.4,'total_income':4006},
    {'date':'2026-04-24','shift':'早班','meituan_rooms':4,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':1,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':3,'meituan_income':768,'ctrip_income':624,'fliggy_income':396,'douyin_income':198,'wechat_income':792,'cash_income':416,'alipay_income':624,'parking_tickets':4,'parking_income':60,'tax':136,'total_rooms':25,'avg_price':145,'occupancy_rate':76.0,'revpgr':110.2,'total_income':3818},
    {'date':'2026-04-25','shift':'早班','meituan_rooms':5,'ctrip_rooms':3,'fliggy_rooms':2,'douyin_rooms':2,'wechat_rooms':4,'cash_rooms':2,'alipay_rooms':4,'meituan_income':960,'ctrip_income':624,'fliggy_income':396,'douyin_income':396,'wechat_income':792,'cash_income':416,'alipay_income':828,'parking_tickets':5,'parking_income':75,'tax':150,'total_rooms':25,'avg_price':146,'occupancy_rate':88.0,'revpgr':128.5,'total_income':4412},
]

SQL = '''
INSERT OR REPLACE INTO daily_reports
(date, shift, meituan_rooms, ctrip_rooms, fliggy_rooms, douyin_rooms,
 wechat_rooms, cash_rooms, alipay_rooms, meituan_income, ctrip_income,
 fliggy_income, douyin_income, wechat_income, cash_income, alipay_income,
 parking_tickets, parking_income, tax, total_rooms, avg_price,
 occupancy_rate, revpgr, total_income, note, uploaded_by)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'seed')
'''

for r in seed_data:
    cur.execute(SQL, (
        r['date'], r.get('shift',''),
        r.get('meituan_rooms',0), r.get('ctrip_rooms',0), r.get('fliggy_rooms',0),
        r.get('douyin_rooms',0), r.get('wechat_rooms',0), r.get('cash_rooms',0),
        r.get('alipay_rooms',0), r.get('meituan_income',0), r.get('ctrip_income',0),
        r.get('fliggy_income',0), r.get('douyin_income',0), r.get('wechat_income',0),
        r.get('cash_income',0), r.get('alipay_income',0), r.get('parking_tickets',0),
        r.get('parking_income',0), r.get('tax',0), r.get('total_rooms',0),
        r.get('avg_price',0), r.get('occupancy_rate',0), r.get('revpgr',0),
        r.get('total_income',0), r.get('note','')
    ))
    print('Inserted:', r['date'])

conn.commit()
count = cur.execute('SELECT COUNT(*) FROM daily_reports').fetchone()[0]
print('Total records:', count)
conn.close()
