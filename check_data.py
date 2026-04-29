# -*- coding: utf-8 -*-
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 用户提供的日报文本格式
sample_text = """
华悦艺术酒店【冠华店】
2026年4月27日
早班: 黄龙英
中班：尹紫玉
晚班：陶金花
总房间数：45间
美团:8间 ：638.08元
携程:3间 ：81.62元
飞猪:0间 ：0元
抖音:0间 ：0元
微信，:24间 ：2430元
现金:1间 ：200元
支付宝:3间 ：100元
补房费（微 ）：30元
超时费（微）：40元
车票（微）：30元
补房卡（微）：30元
水（微）：2元
当日开房累积：41间
平均房价：91.63元
出租率 ：91%
当日Revpgr：83.38元
客房日营业额：3756.3元
总计营业额：3756.3元
特惠大床房：1间：79.2元
精选大床房：13间:899.65元
豪华大床房：15间:1040.48元
城堡亲子房：4间：330元
麻将双床房：6间：758.92元
麻将套房：   0间：0元
 圆床房：1间：74.29元
"""

# 模拟前端的解析逻辑
room_type_keys = [
    '特惠大床房', '精选大床房', '豪华大床房',
    '城堡亲子房', '麻将双床房', '麻将套房', '圆床房'
]

print("Testing room type parsing:")
print("=" * 50)

for name in room_type_keys:
    # JS正则: name + '\\s*[：:]\\s*(\\d+)\\s*间\\s*[：:]\\s*([\\d.]+)\\s*元'
    pattern = name + r'\s*[：:]\s*(\d+)\s*间\s*[：:]\s*([\d.]+)\s*元'
    rx = re.compile(pattern)
    m = rx.search(sample_text)
    if m:
        rooms = int(m.group(1))
        income = float(m.group(2))
        print(f"[OK] {name}: {rooms} rooms, {income} CNY")
    else:
        print(f"[FAIL] {name}: not matched")
