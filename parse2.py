# -*- coding: utf-8 -*-
"""
解析华悦艺术酒店日报，直接输出完整的 seed_data 字典列表
运行: python parse2.py
"""
import re, json

text = open(r"c:\Users\bryan\WorkBuddy\20260426211044\hotel-app\zh_input.txt", encoding='utf-8').read()

# 按日期拆分块
raw = re.split(r'\n\s*华悦艺术酒店【冠华店】\s*\n', text)
raw = [b.strip() for b in raw if b.strip()]

# 通用提取函数
def g_int(block, *keys):
    for k in keys:
        m = re.search(rf'{re.escape(k)}\s*[:：]\s*(\d+)\s*间', block)
        if m: return int(m.group(1))
    return 0

def g_inc(block, *keys):
    for k in keys:
        # 匹配 "美团:7间 ：589.13元" 或 "美团:7间：589.13元"
        m = re.search(rf'{re.escape(k)}\s*[:：]\s*\d+\s*间\s*[:：]\s*(\d+\.?\d*)\s*元', block)
        if not m:
            m = re.search(rf'{re.escape(k)}\s*[:：]\s*(\d+\.?\d*)\s*元', block)
        if m: return float(m.group(1))
    return 0.0

results = []
for block in raw:
    m = re.search(r'2026年(\d+)月(\d+)日', block)
    if not m:
        print(f"SKIP: 无日期: {block[:40]!r}")
        continue
    mm, dd = int(m.group(1)), int(m.group(2))
    date_str = f"2026-{mm:02d}-{dd:02d}"

    shift = '早班'
    if '早班' in block or '早班' in block:
        shift = '早班'

    # 房量
    mr = g_int(block, '美团'); cr = g_int(block, '携程'); fr = g_int(block, '飞猪')
    dr = g_int(block, '抖音'); wr = g_int(block, '微信')
    car = g_int(block, '现金'); ar = g_int(block, '支付宝')
    # 收入
    mi = g_inc(block, '美团'); ci = g_inc(block, '携程'); fi = g_inc(block, '飞猪')
    di = g_inc(block, '抖音'); wi = g_inc(block, '微信')
    cai = g_inc(block, '现金'); ai = g_inc(block, '支付宝')

    # 停车票金额
    park_inc = 0.0
    for m2 in re.finditer(r'(?:停车票|车票)[^：:\n]*[:：]\s*(\d+\.?\d*)\s*元', block):
        park_inc += float(m2.group(1))
    park_t = max(1, int(park_inc / 10)) if park_inc > 0 else 0

    # 税费
    tax = 0.0
    for m2 in re.finditer(r'税费[^：:\n]*[:：]\s*(\d+\.?\d*)', block):
        tax += float(m2.group(1))

    # 统计
    m2 = re.search(r'当日开房累积[：:]\s*(\d+)\s*间', block)
    total_rooms = int(m2.group(1)) if m2 else (mr+cr+fr+dr+wr+car+ar)

    m2 = re.search(r'平均房价[：:]\s*(\d+\.?\d*)\s*元?', block)
    avg_price = float(m2.group(1)) if m2 else 0

    m2 = re.search(r'出租率\s*[：:]\s*(\d+\.?\d*)%?', block)
    occ = float(m2.group(1)) if m2 else 0

    m2 = re.search(r'当日Revpgr[：:]\s*(\d+\.?\d*)\s*元?', block)
    if not m2:
        m2 = re.search(r'Revpgr[：:]\s*(\d+\.?\d*)', block)
    revpgr = float(m2.group(1)) if m2 else 0

    m2 = re.search(r'客房日营业额[：:]\s*(\d+\.?\d*)\s*元?', block)
    if not m2:
        m2 = re.search(r'总计营业额[：:]\s*(\d+\.?\d*)\s*元?', block)
    total_income = float(m2.group(1)) if m2 else 0

    # 房型
    room_types = {}
    for t, key in [('特惠大床房','特惠大床房'),('精选大床房','精选大床房'),
                    ('豪华大床房','豪华大床房'),('城堡亲子房','城堡亲子房'),
                    ('麻将双床房','麻将双床房'),('麻将套房','麻将套房'),
                    ('圆床房','圆床房')]:
        m2 = re.search(rf'{key}\s*[：:]\s*(\d+)\s*间\s*[：:]\s*(\d+\.?\d*)', block)
        if m2:
            room_types[t] = {'rooms': int(m2.group(1)), 'price': float(m2.group(2))}

    results.append({
        'date': date_str, 'shift': shift,
        'meituan_rooms': mr, 'meituan_income': mi,
        'ctrip_rooms': cr, 'ctrip_income': ci,
        'fliggy_rooms': fr, 'fliggy_income': fi,
        'douyin_rooms': dr, 'douyin_income': di,
        'wechat_rooms': wr, 'wechat_income': wi,
        'cash_rooms': car, 'cash_income': cai,
        'alipay_rooms': ar, 'alipay_income': ai,
        'parking_tickets': park_t, 'parking_income': park_inc,
        'tax': tax, 'total_rooms': total_rooms,
        'avg_price': avg_price, 'occupancy_rate': occ,
        'revpgr': revpgr, 'total_income': total_income,
        'room_types': room_types if room_types else None,
    })
    print(f"  OK {date_str} 房={total_rooms} 收={total_income}")

results.sort(key=lambda x: x['date'])
print(f"\n共 {len(results)} 天\n")

# 输出 Python 代码
lines = ["seed_data = ["]
for i, r in enumerate(results):
    rt = json.dumps(r['room_types'], ensure_ascii=False) if r['room_types'] else 'None'
    lines.append("    {'date': '" + r['date'] + "', 'shift': '" + r['shift'] + "',")
    lines.append(f"     'meituan_rooms': {r['meituan_rooms']}, 'meituan_income': {r['meituan_income']},")
    lines.append(f"     'ctrip_rooms': {r['ctrip_rooms']}, 'ctrip_income': {r['ctrip_income']},")
    lines.append(f"     'fliggy_rooms': {r['fliggy_rooms']}, 'fliggy_income': {r['fliggy_income']},")
    lines.append(f"     'douyin_rooms': {r['douyin_rooms']}, 'douyin_income': {r['douyin_income']},")
    lines.append(f"     'wechat_rooms': {r['wechat_rooms']}, 'wechat_income': {r['wechat_income']},")
    lines.append(f"     'cash_rooms': {r['cash_rooms']}, 'cash_income': {r['cash_income']},")
    lines.append(f"     'alipay_rooms': {r['alipay_rooms']}, 'alipay_income': {r['alipay_income']},")
    lines.append(f"     'parking_tickets': {r['parking_tickets']}, 'parking_income': {r['parking_income']},")
    lines.append(f"     'tax': {r['tax']}, 'total_rooms': {r['total_rooms']}, 'avg_price': {r['avg_price']},")
    lines.append(f"     'occupancy_rate': {r['occupancy_rate']}, 'revpgr': {r['revpgr']}, 'total_income': {r['total_income']},")
    lines.append(f"     'room_types': {rt}, 'note': '', 'uploaded_by': 'seed'}}")
    if i < len(results) - 1:
        lines[-1] += ","
lines.append("]")
print("\n".join(lines))
