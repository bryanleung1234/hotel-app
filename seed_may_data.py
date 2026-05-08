#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据导入脚本 - 将2026年5月1-7日数据导入数据库
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import json
import sqlite3

# 2026年5月1-7日的日报数据
REPORTS_DATA = [
    {
        "date": "2026-05-01",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 21, "meituan_income": 2914.08,
        "ctrip_rooms": 9, "ctrip_income": 2583.76,
        "fliggy_rooms": 2, "fliggy_income": 134.72,
        "douyin_rooms": 0, "douyin_income": 0,
        "wechat_rooms": 12, "wechat_income": 1530,
        "cash_rooms": 1, "cash_income": 100,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 30, "parking_income": 67, "tax": 18.1,
        "avg_price": 163.2, "occupancy_rate": 100, "revpgr": 163.2,
        "total_income": 7347.66,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 190.43},
            "精选大床房": {"rooms": 12, "income": 1480.13},
            "豪华大床房": {"rooms": 14, "income": 2132.63},
            "城堡亲子房": {"rooms": 4, "income": 1387.02},
            "麻将双床房": {"rooms": 6, "income": 1577.95},
            "麻将套房": {"rooms": 2, "income": 404.4},
            "圆床房": {"rooms": 1, "income": 120}
        }
    },
    {
        "date": "2026-05-02",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 23, "meituan_income": 1985.48,
        "ctrip_rooms": 11, "ctrip_income": 901.52,
        "fliggy_rooms": 1, "fliggy_income": 198.4,
        "douyin_rooms": 1, "douyin_income": 272.69,
        "wechat_rooms": 11, "wechat_income": 1580,
        "cash_rooms": 1, "cash_income": 110,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 20, "parking_income": 34, "tax": 0,
        "avg_price": 105.8, "occupancy_rate": 100, "revpgr": 112.9,
        "total_income": 5082.09,
        "room_types": {
            "特惠大床房": {"rooms": 3, "income": 295.17},
            "精选大床房": {"rooms": 12, "income": 1100.38},
            "豪华大床房": {"rooms": 19, "income": 1785.1},
            "城堡亲子房": {"rooms": 4, "income": 407.46},
            "麻将双床房": {"rooms": 7, "income": 919.98},
            "麻将套房": {"rooms": 2, "income": 420},
            "圆床房": {"rooms": 1, "income": 120}
        }
    },
    {
        "date": "2026-05-03",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 9, "meituan_income": 522.18,
        "ctrip_rooms": 12, "ctrip_income": 698.2,
        "fliggy_rooms": 3, "fliggy_income": 314.7,
        "douyin_rooms": 1, "douyin_income": 0,
        "wechat_rooms": 12, "wechat_income": 1740,
        "cash_rooms": 2, "cash_income": 260,
        "alipay_rooms": 1, "alipay_income": 200,
        "parking_tickets": 60, "parking_income": 52, "tax": 0,
        "avg_price": 96.1, "occupancy_rate": 88, "revpgr": 85.4,
        "total_income": 3847.08,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 200.31},
            "精选大床房": {"rooms": 12, "income": 1001.82},
            "豪华大床房": {"rooms": 17, "income": 1584.75},
            "城堡亲子房": {"rooms": 4, "income": 150},
            "麻将双床房": {"rooms": 5, "income": 798.2},
            "麻将套房": {"rooms": 0, "income": 0},
            "圆床房": {"rooms": 0, "income": 0}
        }
    },
    {
        "date": "2026-05-04",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 5, "meituan_income": 469.98,
        "ctrip_rooms": 7, "ctrip_income": 609.79,
        "fliggy_rooms": 1, "fliggy_income": 207.2,
        "douyin_rooms": 0, "douyin_income": 0,
        "wechat_rooms": 20, "wechat_income": 2250,
        "cash_rooms": 0, "cash_income": 0,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 10, "parking_income": 20, "tax": 0,
        "avg_price": 108.09, "occupancy_rate": 73, "revpgr": 79.2,
        "total_income": 3566.97,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 156.41},
            "精选大床房": {"rooms": 7, "income": 658.7},
            "豪华大床房": {"rooms": 14, "income": 1290},
            "城堡亲子房": {"rooms": 4, "income": 380.24},
            "麻将双床房": {"rooms": 5, "income": 851.62},
            "麻将套房": {"rooms": 1, "income": 220},
            "圆床房": {"rooms": 0, "income": 0}
        }
    },
    {
        "date": "2026-05-05",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 5, "meituan_income": 396.38,
        "ctrip_rooms": 1, "ctrip_income": 0,
        "fliggy_rooms": 0, "fliggy_income": 0,
        "douyin_rooms": 1, "douyin_income": 119.54,
        "wechat_rooms": 7, "wechat_income": 990,
        "cash_rooms": 0, "cash_income": 0,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 20, "parking_income": 36, "tax": 16,
        "avg_price": 110.1, "occupancy_rate": 28, "revpgr": 34.2,
        "total_income": 1544.92,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 128.4},
            "精选大床房": {"rooms": 2, "income": 185.83},
            "豪华大床房": {"rooms": 6, "income": 661.69},
            "城堡亲子房": {"rooms": 1, "income": 0},
            "麻将双床房": {"rooms": 3, "income": 530},
            "麻将套房": {"rooms": 0, "income": 0},
            "圆床房": {"rooms": 0, "income": 0}
        }
    },
    {
        "date": "2026-05-06",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 7, "meituan_income": 544.46,
        "ctrip_rooms": 1, "ctrip_income": 705.54,
        "fliggy_rooms": 0, "fliggy_income": 0,
        "douyin_rooms": 1, "douyin_income": 248.77,
        "wechat_rooms": 6, "wechat_income": 590,
        "cash_rooms": 2, "cash_income": 300,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 30, "parking_income": 30, "tax": 0,
        "avg_price": 142.2, "occupancy_rate": 37, "revpgr": 53.7,
        "total_income": 2418.47,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 109.29},
            "精选大床房": {"rooms": 5, "income": 528.62},
            "豪华大床房": {"rooms": 5, "income": 459.88},
            "城堡亲子房": {"rooms": 4, "income": 1175.06},
            "麻将双床房": {"rooms": 1, "income": 115.62},
            "麻将套房": {"rooms": 0, "income": 0},
            "圆床房": {"rooms": 0, "income": 0}
        }
    },
    {
        "date": "2026-05-07",
        "shift": "尹紫玉/陶金花/黄龙英",
        "total_rooms": 45,
        "meituan_rooms": 6, "meituan_income": 635.79,
        "ctrip_rooms": 3, "ctrip_income": 100.66,
        "fliggy_rooms": 0, "fliggy_income": 0,
        "douyin_rooms": 1, "douyin_income": 0,
        "wechat_rooms": 6, "wechat_income": 700,
        "cash_rooms": 1, "cash_income": 0,
        "alipay_rooms": 0, "alipay_income": 0,
        "parking_tickets": 30, "parking_income": 32, "tax": 0,
        "avg_price": 77.28, "occupancy_rate": 42, "revpgr": 32.6,
        "total_income": 1468.45,
        "room_types": {
            "特惠大床房": {"rooms": 2, "income": 105.24},
            "精选大床房": {"rooms": 4, "income": 263.25},
            "豪华大床房": {"rooms": 8, "income": 858.6},
            "城堡亲子房": {"rooms": 4, "income": 209.36},
            "麻将双床房": {"rooms": 1, "income": 0},
            "麻将套房": {"rooms": 0, "income": 0},
            "圆床房": {"rooms": 0, "income": 0}
        }
    }
]


def seed_data():
    db_path = os.path.join(os.path.dirname(__file__), 'hotel.db')

    if not os.path.exists(db_path):
        print(f"[ERROR] 数据库不存在: {db_path}")
        print("请先运行 python server.py 初始化数据库")
        return False

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("=" * 50)
    print("开始导入 2026年5月1-7日 日报数据")
    print("=" * 50)

    imported = 0
    skipped = 0

    for r in REPORTS_DATA:
        # 检查是否已存在
        cur.execute("SELECT id FROM daily_reports WHERE date = ?", (r['date'],))
        existing = cur.fetchone()

        room_types_json = json.dumps(r['room_types'], ensure_ascii=False)

        if existing:
            # 更新
            cur.execute('''
                UPDATE daily_reports SET
                    shift = ?,
                    meituan_rooms = ?, meituan_income = ?,
                    ctrip_rooms = ?, ctrip_income = ?,
                    fliggy_rooms = ?, fliggy_income = ?,
                    douyin_rooms = ?, douyin_income = ?,
                    wechat_rooms = ?, wechat_income = ?,
                    cash_rooms = ?, cash_income = ?,
                    alipay_rooms = ?, alipay_income = ?,
                    parking_tickets = ?, parking_income = ?, tax = ?,
                    total_rooms = ?, avg_price = ?,
                    occupancy_rate = ?, revpgr = ?,
                    total_income = ?, room_types = ?
                WHERE date = ?
            ''', (
                r['shift'],
                r['meituan_rooms'], r['meituan_income'],
                r['ctrip_rooms'], r['ctrip_income'],
                r['fliggy_rooms'], r['fliggy_income'],
                r['douyin_rooms'], r['douyin_income'],
                r['wechat_rooms'], r['wechat_income'],
                r['cash_rooms'], r['cash_income'],
                r['alipay_rooms'], r['alipay_income'],
                r['parking_tickets'], r['parking_income'], r['tax'],
                r['total_rooms'], r['avg_price'],
                r['occupancy_rate'], r['revpgr'],
                r['total_income'], room_types_json,
                r['date']
            ))
            print(f"  [更新] {r['date']} - 营业额: ¥{r['total_income']:,.2f}")
        else:
            # 插入
            cur.execute('''
                INSERT INTO daily_reports
                    (date, shift,
                     meituan_rooms, meituan_income,
                     ctrip_rooms, ctrip_income,
                     fliggy_rooms, fliggy_income,
                     douyin_rooms, douyin_income,
                     wechat_rooms, wechat_income,
                     cash_rooms, cash_income,
                     alipay_rooms, alipay_income,
                     parking_tickets, parking_income, tax,
                     total_rooms, avg_price,
                     occupancy_rate, revpgr,
                     total_income, room_types)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                r['date'], r['shift'],
                r['meituan_rooms'], r['meituan_income'],
                r['ctrip_rooms'], r['ctrip_income'],
                r['fliggy_rooms'], r['fliggy_income'],
                r['douyin_rooms'], r['douyin_income'],
                r['wechat_rooms'], r['wechat_income'],
                r['cash_rooms'], r['cash_income'],
                r['alipay_rooms'], r['alipay_income'],
                r['parking_tickets'], r['parking_income'], r['tax'],
                r['total_rooms'], r['avg_price'],
                r['occupancy_rate'], r['revpgr'],
                r['total_income'], room_types_json
            ))
            print(f"  [新增] {r['date']} - 营业额: ¥{r['total_income']:,.2f}")

        imported += 1

    # 清除月度缓存
    cur.execute("DELETE FROM monthly_cache WHERE year = 2026 AND month = 5")

    conn.commit()

    # 统计
    cur.execute("SELECT COUNT(*) as cnt FROM daily_reports")
    total = cur.fetchone()['cnt']

    print("")
    print("=" * 50)
    print(f"导入完成! 本次导入 {imported} 条记录")
    print(f"数据库现有 {total} 条日报")
    print("=" * 50)

    conn.close()
    return True


if __name__ == '__main__':
    seed_data()
