const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = 'hotel-report-secret-key-2024';

// ─── Database Setup ────────────────────────────────────────────────────────
const DB_PATH = path.join(__dirname, 'hotel.db');
const db = new Database(DB_PATH);

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE NOT NULL,
    name TEXT,
    role TEXT NOT NULL DEFAULT 'staff',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS daily_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    shift TEXT,
    meituan_rooms INTEGER DEFAULT 0,
    ctrip_rooms INTEGER DEFAULT 0,
    fliggy_rooms INTEGER DEFAULT 0,
    douyin_rooms INTEGER DEFAULT 0,
    wechat_rooms INTEGER DEFAULT 0,
    cash_rooms INTEGER DEFAULT 0,
    alipay_rooms INTEGER DEFAULT 0,
    meituan_income REAL DEFAULT 0,
    ctrip_income REAL DEFAULT 0,
    fliggy_income REAL DEFAULT 0,
    douyin_income REAL DEFAULT 0,
    wechat_income REAL DEFAULT 0,
    cash_income REAL DEFAULT 0,
    alipay_income REAL DEFAULT 0,
    parking_tickets INTEGER DEFAULT 0,
    parking_income REAL DEFAULT 0,
    tax REAL DEFAULT 0,
    total_rooms INTEGER DEFAULT 0,
    avg_price REAL DEFAULT 0,
    occupancy_rate REAL DEFAULT 0,
    revpgr REAL DEFAULT 0,
    total_income REAL DEFAULT 0,
    note TEXT,
    uploaded_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
  );

  CREATE TABLE IF NOT EXISTS monthly_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    data TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(year, month)
  );

  CREATE TABLE IF NOT EXISTS login_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    role TEXT,
    ip TEXT,
    ua TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

// Seed users if not exist
const upsertUser = db.prepare(`
  INSERT OR IGNORE INTO users (phone, name, role) VALUES (?, ?, ?)
`);
upsertUser.run('19128957480', '员工', 'staff');
upsertUser.run('13802531098', '老板A', 'boss');
upsertUser.run('18602032126', '老板B', 'boss');

// ─── Middleware ────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.static(path.join(__dirname, 'public')));

// Auth middleware
function authenticate(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith('Bearer ')) {
    return res.status(401).json({ error: '未登录，请先登录' });
  }
  try {
    const token = auth.slice(7);
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (e) {
    return res.status(401).json({ error: '登录已过期，请重新登录' });
  }
}

function requireBoss(req, res, next) {
  if (req.user.role !== 'boss') {
    return res.status(403).json({ error: '权限不足，仅老板可访问' });
  }
  next();
}

// ─── Auth Routes ────────────────────────────────────────────────────────────
app.post('/api/auth/login', (req, res) => {
  const { phone, code } = req.body;
  if (!phone || !code) {
    return res.status(400).json({ error: '手机号和验证码必填' });
  }
  if (String(code).length !== 6) {
    return res.status(400).json({ error: '验证码为6位数字' });
  }

  const user = db.prepare('SELECT * FROM users WHERE phone = ?').get(phone);
  if (!user) {
    return res.status(401).json({ error: '该手机号未注册' });
  }

  const token = jwt.sign(
    { id: user.id, phone: user.phone, role: user.role, name: user.name },
    JWT_SECRET,
    { expiresIn: '30d' }
  );

  // Log login
  db.prepare(`
    INSERT INTO login_log (phone, role, ip, ua) VALUES (?, ?, ?, ?)
  `).run(phone, user.role, req.ip, req.headers['user-agent'] || '');

  res.json({
    token,
    user: { id: user.id, phone: user.phone, role: user.role, name: user.name }
  });
});

app.get('/api/auth/me', authenticate, (req, res) => {
  res.json({ user: req.user });
});

// ─── Report Upload Routes ──────────────────────────────────────────────────
app.post('/api/reports/upload', authenticate, (req, res) => {
  const { reports } = req.body;
  if (!reports || !Array.isArray(reports)) {
    return res.status(400).json({ error: '缺少 reports 数据' });
  }

  const insertReport = db.prepare(`
    INSERT OR REPLACE INTO daily_reports
    (date, shift, meituan_rooms, ctrip_rooms, fliggy_rooms, douyin_rooms,
     wechat_rooms, cash_rooms, alipay_rooms, meituan_income, ctrip_income,
     fliggy_income, douyin_income, wechat_income, cash_income, alipay_income,
     parking_tickets, parking_income, tax, total_rooms, avg_price,
     occupancy_rate, revpgr, total_income, note, uploaded_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const insertMany = db.transaction((items) => {
    for (const r of items) {
      insertReport.run(
        r.date, r.shift || '', r.meituan_rooms || 0, r.ctrip_rooms || 0,
        r.fliggy_rooms || 0, r.douyin_rooms || 0, r.wechat_rooms || 0,
        r.cash_rooms || 0, r.alipay_rooms || 0, r.meituan_income || 0,
        r.ctrip_income || 0, r.fliggy_income || 0, r.douyin_income || 0,
        r.wechat_income || 0, r.cash_income || 0, r.alipay_income || 0,
        r.parking_tickets || 0, r.parking_income || 0, r.tax || 0,
        r.total_rooms || 0, r.avg_price || 0, r.occupancy_rate || 0,
        r.revpgr || 0, r.total_income || 0, r.note || '', req.user.phone
      );
    }
  });

  insertMany(reports);

  // Invalidate monthly cache for affected months
  const months = [...new Set(reports.map(r => r.date.slice(0, 7)))];
  const deleteCache = db.prepare('DELETE FROM monthly_cache WHERE year = ? AND month = ?');
  const invalidate = db.transaction((ms) => {
    for (const m of ms) {
      const [y, mo] = m.split('-').map(Number);
      deleteCache.run(y, mo);
    }
  });
  invalidate(months);

  res.json({ success: true, count: reports.length });
});

// ─── Report Query Routes ───────────────────────────────────────────────────
app.get('/api/reports', authenticate, requireBoss, (req, res) => {
  const { year, month } = req.query;
  let sql = 'SELECT * FROM daily_reports ORDER BY date DESC';
  const params = [];

  if (year && month) {
    sql = 'SELECT * FROM daily_reports WHERE date LIKE ? ORDER BY date DESC';
    params.push(`${year}-${String(month).padStart(2, '0')}%`);
  } else if (year) {
    sql = 'SELECT * FROM daily_reports WHERE date LIKE ? ORDER BY date DESC';
    params.push(`${year}%`);
  }

  const reports = db.prepare(sql).all(...params);
  res.json({ reports });
});

app.get('/api/reports/monthly', authenticate, requireBoss, (req, res) => {
  const { year, month } = req.query;
  if (!year || !month) {
    return res.status(400).json({ error: '缺少 year 或 month 参数' });
  }

  const yearInt = parseInt(year);
  const monthInt = parseInt(month);
  const paddedMonth = String(monthInt).padStart(2, '0');

  // Check cache first
  const cached = db.prepare(
    'SELECT data FROM monthly_cache WHERE year = ? AND month = ?'
  ).get(yearInt, monthInt);

  if (cached) {
    return res.json(JSON.parse(cached.data));
  }

  // Build monthly data from daily reports
  const reports = db.prepare(`
    SELECT * FROM daily_reports
    WHERE date LIKE ?
    ORDER BY date ASC
  `).all(`${yearInt}-${paddedMonth}%`);

  if (reports.length === 0) {
    return res.json({ year: yearInt, month: monthInt, reports: [], summary: null });
  }

  // Compute summary
  const totalDays = reports.length;
  const totalRooms = reports.reduce((s, r) => s + (r.total_rooms || 0), 0);
  const totalIncome = reports.reduce((s, r) => s + (r.total_income || 0), 0);
  const avgIncome = totalIncome / totalDays;
  const avgOccupancy = reports.reduce((s, r) => s + (r.occupancy_rate || 0), 0) / totalDays;
  const avgRevpgr = reports.reduce((s, r) => s + (r.revpgr || 0), 0) / totalDays;
  const totalTax = reports.reduce((s, r) => s + (r.tax || 0), 0);
  const totalParking = reports.reduce((s, r) => s + (r.parking_income || 0), 0);

  // Channel analysis
  const channelData = {
    meituan: { rooms: 0, income: 0 },
    ctrip: { rooms: 0, income: 0 },
    fliggy: { rooms: 0, income: 0 },
    douyin: { rooms: 0, income: 0 },
    wechat: { rooms: 0, income: 0 },
    cash: { rooms: 0, income: 0 },
    alipay: { rooms: 0, income: 0 }
  };
  for (const r of reports) {
    channelData.meituan.rooms += r.meituan_rooms || 0;
    channelData.meituan.income += r.meituan_income || 0;
    channelData.ctrip.rooms += r.ctrip_rooms || 0;
    channelData.ctrip.income += r.ctrip_income || 0;
    channelData.fliggy.rooms += r.fliggy_rooms || 0;
    channelData.fliggy.income += r.fliggy_income || 0;
    channelData.douyin.rooms += r.douyin_rooms || 0;
    channelData.douyin.income += r.douyin_income || 0;
    channelData.wechat.rooms += r.wechat_rooms || 0;
    channelData.wechat.income += r.wechat_income || 0;
    channelData.cash.rooms += r.cash_rooms || 0;
    channelData.cash.income += r.cash_income || 0;
    channelData.alipay.rooms += r.alipay_rooms || 0;
    channelData.alipay.income += r.alipay_income || 0;
  }

  // Weekly breakdown
  const weeks = [[], [], [], [], []];
  for (const r of reports) {
    const day = parseInt(r.date.split('-')[2]);
    const weekIdx = Math.min(Math.floor((day - 1) / 7), 4);
    weeks[weekIdx].push(r);
  }
  const weeklyData = weeks.filter(w => w.length > 0).map((wr, i) => ({
    week: `第${i + 1}周`, count: wr.length,
    income: wr.reduce((s, r) => s + (r.total_income || 0), 0),
    occupancy: wr.reduce((s, r) => s + (r.occupancy_rate || 0), 0) / wr.length
  }));

  // Daily trend
  const dailyTrend = reports.map(r => ({
    date: r.date, income: r.total_income || 0, occupancy: r.occupancy_rate || 0,
    revpgr: r.revpgr || 0, rooms: r.total_rooms || 0
  }));

  const result = {
    year: yearInt, month: monthInt, reportCount: totalDays,
    summary: {
      totalIncome, avgIncome, avgOccupancy, avgRevpgr, totalTax, totalParking,
      channelData, weeklyData, dailyTrend
    },
    reports
  };

  // Cache it
  db.prepare(`
    INSERT OR REPLACE INTO monthly_cache (year, month, data, updated_at)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
  `).run(yearInt, monthInt, JSON.stringify(result));

  res.json(result);
});

app.get('/api/reports/dates', authenticate, (req, res) => {
  const dates = db.prepare(
    'SELECT DISTINCT date FROM daily_reports ORDER BY date DESC'
  ).all().map(r => r.date);
  res.json({ dates });
});

app.get('/api/reports/stats', authenticate, requireBoss, (req, res) => {
  const totalReports = db.prepare('SELECT COUNT(*) as c FROM daily_reports').get().c;
  const totalIncome = db.prepare('SELECT SUM(total_income) as s FROM daily_reports').get().s || 0;
  const latestDate = db.prepare('SELECT MAX(date) as d FROM daily_reports').get().d;
  res.json({ totalReports, totalIncome, latestDate });
});

// ─── Serve Frontend ─────────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🏨 酒店日报系统已启动: http://localhost:${PORT}`);
  console.log(`📊 数据库: ${DB_PATH}`);
  console.log(`👤 员工登录: 19128957480`);
  console.log(`👤 老板登录: 13802531098 / 18602032126`);
});
