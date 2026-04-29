'use strict';

// ─── Auth ────────────────────────────────────────────────────────────────────
const Auth = {
  TOKEN_KEY: 'hotel_token',
  USER_KEY: 'hotel_user',

  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  },
  getUser() {
    const u = localStorage.getItem(this.USER_KEY);
    return u ? JSON.parse(u) : null;
  },
  setSession(token, user) {
    localStorage.setItem(this.TOKEN_KEY, token);
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  },
  clear() {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
  },
  isBoss() {
    const u = this.getUser();
    return u && u.role === 'boss';
  },
  isStaff() {
    const u = this.getUser();
    return u && u.role === 'staff';
  },
  getAuthHeader() {
    const t = this.getToken();
    return t ? { 'Authorization': `Bearer ${t}` } : {};
  }
};

// ─── API Client ──────────────────────────────────────────────────────────────
const API = {
  base: '/api',

  async request(method, path, body = null) {
    const opts = { method, headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeader() } };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(this.base + path, opts);
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || `请求失败 (${r.status})`);
    return data;
  },

  login(phone, code) { return this.request('POST', '/auth/login', { phone, code }); },
  getMe() { return this.request('GET', '/auth/me'); },

  async uploadReports(reports) {
    return this.request('POST', '/reports/upload', { reports });
  },
  getReports(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request('GET', '/reports' + (qs ? '?' + qs : ''));
  },
  getMonthly(year, month) { return this.request('GET', `/reports/monthly?year=${year}&month=${month}`); },
  getDates() { return this.request('GET', '/reports/dates'); },
  getStats() { return this.request('GET', '/reports/stats'); }
};

// ─── Text Parser ────────────────────────────────────────────────────────────
// 精确匹配华悦艺术酒店冠华店日报格式
// 格式示例：
//   美团:8间 ：638.08元
//   车票（微）：30元
//   当日开房累积：39间
//   平均房价：91.63元   出租率 ：86%   当日Revpgr：79.41元
const Parser = {
  HOTEL_NAMES: ['华悦艺术酒店'],

  parseText(text) {
    const blocks = this.splitBlocks(text);
    return blocks.map(b => this.parseBlock(b)).filter(Boolean);
  },

  // 按"华悦艺术酒店"或日期行拆分多天日报
  splitBlocks(text) {
    const blocks = [];
    let current = '';
    const lines = text.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      const isHotelLine = this.HOTEL_NAMES.some(n => trimmed.includes(n)) && trimmed.length < 60;
      const isDateLine = /^\d{4}[-/年]\d{1,2}[-/月]\d{1,2}/.test(trimmed) && trimmed.length < 30;

      if (isHotelLine || isDateLine) {
        if (current.trim()) blocks.push(current.trim());
        current = line;
      } else {
        current += '\n' + line;
      }
    }
    if (current.trim()) blocks.push(current.trim());
    return blocks.filter(b => b.trim());
  },

  parseBlock(text) {
    const date = this.extractDate(text);
    if (!date) return null;

    const shift      = this.extractShift(text);
    const channels   = this.extractChannels(text);
    const parking    = this.extractParking(text);
    const tax        = this.extractTax(text);
    const kpi        = this.extractKPI(text);
    const roomTypes  = this.extractRoomTypes(text);

    return {
      date,
      shift,
      meituan_rooms:  channels.rooms.meituan  || 0,
      ctrip_rooms:    channels.rooms.ctrip    || 0,
      fliggy_rooms:   channels.rooms.fliggy   || 0,
      douyin_rooms:   channels.rooms.douyin   || 0,
      wechat_rooms:   channels.rooms.wechat   || 0,
      cash_rooms:     channels.rooms.cash     || 0,
      alipay_rooms:   channels.rooms.alipay   || 0,
      meituan_income: channels.incomes.meituan || 0,
      ctrip_income:   channels.incomes.ctrip   || 0,
      fliggy_income:  channels.incomes.fliggy  || 0,
      douyin_income:  channels.incomes.douyin  || 0,
      wechat_income:  channels.incomes.wechat  || 0,
      cash_income:    channels.incomes.cash    || 0,
      alipay_income:  channels.incomes.alipay  || 0,
      parking_tickets: parking.tickets || 0,
      parking_income:  parking.income  || 0,
      tax: tax || 0,
      total_rooms:     kpi.totalRooms     || 0,
      avg_price:       kpi.avgPrice       || 0,
      occupancy_rate:  kpi.occupancyRate  || 0,
      revpgr:          kpi.revpgr         || 0,
      total_income:    kpi.totalIncome    || 0,
      room_types:      roomTypes,
      note: ''
    };
  },

  // 提取日期
  extractDate(text) {
    const m = text.match(/(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})/);
    if (!m) return null;
    return `${m[1]}-${m[2].padStart(2,'0')}-${m[3].padStart(2,'0')}`;
  },

  // 提取班次：日报包含早/中/晚三班，记录为"早中晚班"
  extractShift(text) {
    const hasEarly = /早班/.test(text);
    const hasMid   = /中班/.test(text);
    const hasNight = /晚班/.test(text);
    if (hasEarly && hasMid && hasNight) return '全天';
    if (hasEarly) return '早班';
    if (hasMid)   return '中班';
    if (hasNight) return '晚班';
    return '';
  },

  // 提取各渠道房间数和收入
  // 格式：美团:8间 ：638.08元  （中英文冒号混用，间后面跟收入）
  extractChannels(text) {
    const rooms   = {};
    const incomes = {};

    // 渠道关键词映射
    const channelMap = [
      { key: 'meituan', kws: ['美团'] },
      { key: 'ctrip',   kws: ['携程'] },
      { key: 'fliggy',  kws: ['飞猪'] },
      { key: 'douyin',  kws: ['抖音'] },
      { key: 'wechat',  kws: ['微信，', '微信,', '微信'] },  // 注意"微信，"的逗号变体
      { key: 'cash',    kws: ['现金'] },
      { key: 'alipay',  kws: ['支付宝', '支附宝', '支附'] },
    ];

    // 额外收入行（补房费/超时费/水费等），累加到微信收入
    // 格式：补房费（微 ）：30元   超时费（微）：40元
    const extraWechatRx = /(?:补房费|超时费|补房卡|水费?|水)\s*[（(][^)）]*[)）]\s*[：:]\s*([\d.]+)\s*元/g;

    const lines = text.split('\n');

    for (const line of lines) {
      const l = line.trim();
      if (!l) continue;

      // 匹配渠道行：渠道名 冒号 房间数间 冒号 金额元
      // 例：美团:8间 ：638.08元   微信，:24间 ：2430元
      for (const { key, kws } of channelMap) {
        if (rooms[key] !== undefined) continue; // 已匹配过
        for (const kw of kws) {
          // 房间数：关键词后跟冒号（中英文）再跟数字+间
          const roomRx = new RegExp(kw + '[^\\d\\n]*?(\\d+)\\s*间');
          const rm = l.match(roomRx);
          if (!rm) continue;

          // 收入：同行中第一个 数字+元（中英文冒号后）
          const incomeRx = /[：:]\s*([\d.]+)\s*元/g;
          let im;
          let lastIncome = null;
          while ((im = incomeRx.exec(l)) !== null) {
            lastIncome = parseFloat(im[1]);
          }

          rooms[key]   = parseInt(rm[1]);
          incomes[key] = lastIncome || 0;
          break;
        }
      }
    }

    // 累加微信额外收入行（补房费/超时费等）
    let extraWechat = 0;
    let em;
    while ((em = extraWechatRx.exec(text)) !== null) {
      extraWechat += parseFloat(em[1]) || 0;
    }
    if (extraWechat > 0) {
      incomes.wechat = (incomes.wechat || 0) + extraWechat;
    }

    // 车票收入也单独计，不计入渠道（由 extractParking 处理）

    return { rooms, incomes };
  },

  // 提取停车/车票信息
  // 格式：车票（微）：30元
  extractParking(text) {
    // 张数（如有）
    const ticketCountRx = /车票[^0-9\n]*?(\d+)\s*张/;
    const tm = text.match(ticketCountRx);
    const tickets = tm ? parseInt(tm[1]) : 0;

    // 车票收入
    const incomeRx = /车票[^0-9\n]*?[：:]\s*([\d.]+)\s*元/;
    const im = text.match(incomeRx);
    const income = im ? parseFloat(im[1]) : 0;

    return { tickets, income };
  },

  // 提取税费信息
  // 格式：税：XXX元
  extractTax(text) {
    const taxRx = /税[：:]\s*([\d.]+)\s*元/;
    const m = text.match(taxRx);
    return m ? parseFloat(m[1]) : 0;
  },

  // 提取日报 KPI（直接读取日报文本中的汇总数据，不重新计算）
  // 当日开房累积：39间
  // 平均房价：91.63元
  // 出租率 ：86%
  // 当日Revpgr：79.41元
  // 客房日营业额：3573.7元  /  总计营业额：3573.7元
  extractKPI(text) {
    // 当日实际开房数（优先）
    const totalRoomsRx = /当日开房[^0-9\n]*?(\d+)\s*间/;
    let totalRooms = 0;
    const trm = text.match(totalRoomsRx);
    if (trm) {
      totalRooms = parseInt(trm[1]);
    } else {
      // 退路：总房间数
      const fallback = text.match(/总房间数[^0-9\n]*?(\d+)\s*间/);
      if (fallback) totalRooms = parseInt(fallback[1]);
    }

    // 平均房价（日）：取"平均房价：91.63元"中的第一个
    const avgPriceRx = /平均房价[^0-9\n]*?([\d.]+)\s*元/;
    const apm = text.match(avgPriceRx);
    const avgPrice = apm ? parseFloat(apm[1]) : 0;

    // 出租率：86%
    const occupancyRx = /出租率[^0-9\n]*?([\d.]+)\s*%/;
    const ocm = text.match(occupancyRx);
    const occupancyRate = ocm ? parseFloat(ocm[1]) : 0;

    // 当日 RevPGR（含"当日"前缀优先，防止和月数据混淆）
    const revpgrRx = /当日\s*[Rr]evpgr[^0-9\n]*?([\d.]+)/i;
    const revpgrRxFallback = /[Rr]evpgr[^0-9\n]*?([\d.]+)/i;
    let revpgr = 0;
    const rvm = text.match(revpgrRx) || text.match(revpgrRxFallback);
    if (rvm) revpgr = parseFloat(rvm[1]);

    // 当日总营业额：优先"客房日营业额"，其次"总计营业额"
    // 注意月营业额在后面，取第一个匹配
    const incomeRx = /(?:客房日营业额|当日营业额)[^0-9\n]*?([\d.]+)\s*元/;
    const incomeRxFallback = /总计营业额[^0-9\n]*?([\d.]+)\s*元/;
    let totalIncome = 0;
    const iim = text.match(incomeRx) || text.match(incomeRxFallback);
    if (iim) totalIncome = parseFloat(iim[1]);

    return { totalRooms, avgPrice, occupancyRate, revpgr, totalIncome };
  },

  // 提取房型明细
  // 格式：特惠大床房：1间：67.36元  （房名：数字间：金额元）
  extractRoomTypes(text) {
    const roomTypes = {};
    const roomTypeKeys = [
      '特惠大床房', '精选大床房', '豪华大床房',
      '城堡亲子房', '麻将双床房', '麻将套房', '圆床房'
    ];
    for (const name of roomTypeKeys) {
      // 匹配：房名 + 冒号 + 数字 + 间 + 冒号 + 金额 + 元
      const rx = new RegExp(name + '\\s*[：:]\\s*(\\d+)\\s*间\\s*[：:]\\s*([\\d.]+)\\s*元');
      const m = text.match(rx);
      if (m) {
        roomTypes[name] = {
          rooms: parseInt(m[1]),
          income: parseFloat(m[2])
        };
      } else {
        // 备用匹配：房名 + 数字 + 间 + : + 金额元（无第二冒号）
        const rx2 = new RegExp(name + '\\s*[：:]\\s*(\\d+)\\s*间\\s*[：:]\\s*([\\d.]+)\\s*元');
        const m2 = text.match(rx2);
        if (m2) {
          roomTypes[name] = {
            rooms: parseInt(m2[1]),
            income: parseFloat(m2[2])
          };
        }
      }
    }
    return roomTypes;
  }
};

// ─── Formatter ──────────────────────────────────────────────────────────────
const Fmt = {
  currency(v) { return (v || 0).toLocaleString('zh-CN', { minimumFractionDigits: 1, maximumFractionDigits: 1 }); },
  pct(v) { return (v || 0).toFixed(1); },
  num(v) { return (v || 0).toLocaleString('zh-CN'); },
  date(d) {
    if (!d) return '—';
    const [y, mo, day] = d.split('-');
    return `${parseInt(y)}年${parseInt(mo)}月${parseInt(day)}日`;
  },
  shortDate(d) {
    if (!d) return '—';
    const [, mo, day] = d.split('-');
    return `${parseInt(mo)}/${parseInt(day)}`;
  }
};

// ─── Chart.js CDN (loaded dynamically) ─────────────────────────────────────
function ensureChartJs() {
  if (window.Chart) return Promise.resolve();
  return new Promise((resolve) => {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
    s.onload = resolve;
    document.head.appendChild(s);
  });
}

// ─── Router ─────────────────────────────────────────────────────────────────
function go(page, params = '') {
  window.location.href = page + '.html' + (params ? '?' + params : '');
}

function getRoleFromURL() {
  const u = Auth.getUser();
  if (!u) { go('index'); return null; }
  return u;
}

function requireRole(role) {
  const u = getRoleFromURL();
  if (!u) return null;
  if (role === 'boss' && u.role !== 'boss') {
    alert('权限不足，仅老板可访问此页面');
    go('staff');
    return null;
  }
  return u;
}
