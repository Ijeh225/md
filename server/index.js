import 'dotenv/config'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import bcrypt from 'bcryptjs'
import compression from 'compression'
import express from 'express'
import helmet from 'helmet'
import jwt from 'jsonwebtoken'
import morgan from 'morgan'
import pg from 'pg'
import { notifications as seedNotifications, payments as seedPayments, users as seedUsers, wallets as seedWallets } from './seedData.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.join(__dirname, '..')
const distDir = path.join(rootDir, 'dist')
const port = process.env.PORT || 3000
const jwtSecret = process.env.JWT_SECRET || 'local-development-secret'
const mdInitialPassword = process.env.MD_INITIAL_PASSWORD || 'ChangeMe123!'
const assistantInitialPassword = process.env.ASSISTANT_INITIAL_PASSWORD || 'Assistant123!'

const app = express()
const pool = process.env.DATABASE_URL
  ? new pg.Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
    })
  : null

const memory = {
  users: [],
  payments: structuredClone(seedPayments),
  wallets: structuredClone(seedWallets),
  notifications: seedNotifications.map((notification, index) => ({ id: index + 1, ...notification })),
  audit: [],
}

app.use(morgan('tiny'))
app.use(compression())
app.use(express.json({ limit: '2mb' }))
app.use(
  helmet({
    contentSecurityPolicy: false,
    crossOriginEmbedderPolicy: false,
  }),
)

app.get('/api/health', (_request, response) => {
  response.json({ ok: true, database: pool ? 'postgres' : 'memory' })
})

app.post('/api/auth/login', async (request, response) => {
  const { userId, password } = request.body
  const user = await findUser(userId)
  if (!user || !(await bcrypt.compare(password || '', user.password_hash))) {
    return response.status(401).json({ message: 'Invalid login details' })
  }
  const token = jwt.sign({ sub: user.id, role: user.role, name: user.name }, jwtSecret, { expiresIn: '12h' })
  response.json({ token, user: publicUser(user) })
})

app.get('/api/bootstrap', authenticate, async (request, response) => {
  response.json(await getBootstrap(request.user))
})

app.patch('/api/payments/:id', authenticate, requireMd, async (request, response) => {
  const { action, updates = {} } = request.body
  const payment = await updatePayment(request.params.id, action || 'Updated', updates, request.user)
  if (!payment) return response.status(404).json({ message: 'Payment not found' })
  response.json(await getBootstrap(request.user))
})

app.post('/api/payments/:id/comments', authenticate, async (request, response) => {
  const text = String(request.body.text || '').trim()
  if (!text) return response.status(400).json({ message: 'Comment text is required' })
  const payment = await addPaymentComment(request.params.id, text, request.user)
  if (!payment) return response.status(404).json({ message: 'Payment not found' })
  response.json(await getBootstrap(request.user))
})

app.patch('/api/notifications/:id/read', authenticate, async (request, response) => {
  await markNotificationRead(request.params.id)
  response.json(await getBootstrap(request.user))
})

app.use(express.static(distDir))
app.get('*', (_request, response) => {
  response.sendFile(path.join(distDir, 'index.html'))
})

await initializeStore()

app.listen(port, () => {
  console.log(`MD finance control server running on ${port}`)
})

async function initializeStore() {
  if (!pool) {
    const mdHash = await bcrypt.hash(mdInitialPassword, 10)
    const assistantHash = await bcrypt.hash(assistantInitialPassword, 10)
    memory.users = seedUsers.map((user) => ({ ...user, password_hash: user.role === 'md' ? mdHash : assistantHash }))
    memory.audit = buildSeedAudit(memory.payments)
    console.log('DATABASE_URL not set; using in-memory development store')
    return
  }

  await pool.query(`
    create table if not exists app_users (
      id text primary key,
      name text not null,
      title text not null,
      role text not null,
      password_hash text not null,
      created_at timestamptz not null default now()
    );

    create table if not exists wallets (
      id bigserial primary key,
      name text not null unique,
      balance numeric not null,
      limit_amount numeric not null,
      user_id text references app_users(id)
    );

    create table if not exists payments (
      id text primary key,
      vendor text not null,
      contact text,
      user_id text references app_users(id),
      description text not null,
      amount numeric not null,
      paid numeric not null default 0,
      scheduled_date text not null,
      due_bucket text not null,
      wallet text not null,
      priority text not null,
      status text not null,
      created_by text not null,
      attachment text,
      created_at_label text,
      last_payment text,
      previous_payments numeric not null default 0,
      proof text,
      comments jsonb not null default '[]',
      timeline jsonb not null default '[]',
      updated_at timestamptz not null default now()
    );

    create table if not exists notifications (
      id bigserial primary key,
      type text not null,
      text text not null,
      target text,
      unread boolean not null default true,
      created_at timestamptz not null default now()
    );

    create table if not exists audit_events (
      id bigserial primary key,
      actor text not null,
      action text not null,
      ref text not null,
      detail text not null,
      created_at timestamptz not null default now()
    );
  `)

  const count = Number((await pool.query('select count(*) from app_users')).rows[0].count)
  if (count > 0) return

  const mdHash = await bcrypt.hash(mdInitialPassword, 10)
  const assistantHash = await bcrypt.hash(assistantInitialPassword, 10)

  for (const user of seedUsers) {
    await pool.query(
      'insert into app_users (id, name, title, role, password_hash) values ($1, $2, $3, $4, $5)',
      [user.id, user.name, user.title, user.role, user.role === 'md' ? mdHash : assistantHash],
    )
  }

  for (const wallet of seedWallets) {
    await pool.query(
      'insert into wallets (name, balance, limit_amount, user_id) values ($1, $2, $3, $4)',
      [wallet.name, wallet.balance, wallet.limit, wallet.userId],
    )
  }

  for (const payment of seedPayments) {
    await pool.query(
      `insert into payments (
        id, vendor, contact, user_id, description, amount, paid, scheduled_date, due_bucket, wallet,
        priority, status, created_by, attachment, created_at_label, last_payment, previous_payments,
        proof, comments, timeline
      ) values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20)`,
      [
        payment.id,
        payment.vendor,
        payment.contact,
        payment.userId,
        payment.description,
        payment.amount,
        payment.paid,
        payment.scheduledDate,
        payment.dueBucket,
        payment.wallet,
        payment.priority,
        payment.status,
        payment.createdBy,
        payment.attachment,
        payment.createdAt,
        payment.lastPayment,
        payment.previousPayments,
        payment.proof,
        JSON.stringify(payment.comments),
        JSON.stringify(payment.timeline),
      ],
    )
  }

  for (const notification of seedNotifications) {
    await pool.query('insert into notifications (type, text, target, unread) values ($1, $2, $3, $4)', [
      notification.type,
      notification.text,
      notification.target,
      notification.unread,
    ])
  }

  for (const event of buildSeedAudit(seedPayments)) {
    await pool.query('insert into audit_events (actor, action, ref, detail) values ($1, $2, $3, $4)', [
      event.actor,
      event.action,
      event.ref,
      event.detail,
    ])
  }
}

async function findUser(id) {
  if (!pool) return memory.users.find((user) => user.id === id)
  return (await pool.query('select * from app_users where id = $1', [id])).rows[0]
}

async function getBootstrap(user) {
  if (!pool) {
    return {
      users: publicUsers(memory.users),
      payments: memory.payments,
      wallets: memory.wallets,
      notifications: memory.notifications,
      audit: memory.audit,
      currentUser: user,
    }
  }

  const [usersResult, paymentsResult, walletsResult, notificationsResult, auditResult] = await Promise.all([
    pool.query('select id, name, title, role from app_users order by role desc, name asc'),
    pool.query('select * from payments order by updated_at desc, id asc'),
    pool.query('select name, balance, limit_amount, user_id from wallets order by name asc'),
    pool.query('select id, type, text, target, unread from notifications order by created_at desc limit 50'),
    pool.query(`select to_char(created_at, 'YYYY-MM-DD HH24:MI') as time, actor, action, ref, detail from audit_events order by created_at desc limit 200`),
  ])

  return {
    users: usersResult.rows.map(publicUser),
    payments: paymentsResult.rows.map(fromDbPayment),
    wallets: walletsResult.rows.map((wallet) => ({
      name: wallet.name,
      balance: Number(wallet.balance),
      limit: Number(wallet.limit_amount),
      userId: wallet.user_id,
    })),
    notifications: notificationsResult.rows,
    audit: auditResult.rows,
    currentUser: user,
  }
}

async function updatePayment(id, action, updates, user) {
  const stamped = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  if (!pool) {
    const index = memory.payments.findIndex((payment) => payment.id === id)
    if (index === -1) return null
    const payment = memory.payments[index]
    memory.payments[index] = { ...payment, ...updates, timeline: [`${action} by ${user.name} at ${stamped}`, ...payment.timeline] }
    memory.notifications.unshift({ id: Date.now(), type: 'approval', text: `${action} for ${payment.vendor}`, target: id, unread: true })
    memory.audit.unshift({ time: 'Recent', actor: user.name, action, ref: id, detail: `${action} for ${payment.vendor}` })
    return memory.payments[index]
  }

  const current = (await pool.query('select * from payments where id = $1', [id])).rows[0]
  if (!current) return null
  const next = { ...fromDbPayment(current), ...updates }
  next.timeline = [`${action} by ${user.name} at ${stamped}`, ...next.timeline]

  await pool.query(
    `update payments set paid = $2, scheduled_date = $3, wallet = $4, priority = $5, status = $6, timeline = $7, updated_at = now() where id = $1`,
    [id, next.paid, next.scheduledDate, next.wallet, next.priority, next.status, JSON.stringify(next.timeline)],
  )
  await pool.query('insert into notifications (type, text, target, unread) values ($1, $2, $3, true)', [
    'approval',
    `${action} for ${next.vendor}`,
    id,
  ])
  await pool.query('insert into audit_events (actor, action, ref, detail) values ($1, $2, $3, $4)', [
    user.name,
    action,
    id,
    `${action} for ${next.vendor}`,
  ])
  return next
}

async function addPaymentComment(id, text, user) {
  const stamped = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  if (!pool) {
    const index = memory.payments.findIndex((payment) => payment.id === id)
    if (index === -1) return null
    const payment = memory.payments[index]
    memory.payments[index] = {
      ...payment,
      comments: [{ by: user.name, text, at: stamped }, ...payment.comments],
      timeline: [`${user.name} commented: ${text}`, ...payment.timeline],
    }
    memory.notifications.unshift({ id: Date.now(), type: 'comment', text: `${user.name} commented on ${payment.vendor}`, target: id, unread: true })
    memory.audit.unshift({ time: 'Recent', actor: user.name, action: 'Commented', ref: id, detail: text })
    return memory.payments[index]
  }

  const current = (await pool.query('select * from payments where id = $1', [id])).rows[0]
  if (!current) return null
  const payment = fromDbPayment(current)
  payment.comments = [{ by: user.name, text, at: stamped }, ...payment.comments]
  payment.timeline = [`${user.name} commented: ${text}`, ...payment.timeline]
  await pool.query('update payments set comments = $2, timeline = $3, updated_at = now() where id = $1', [
    id,
    JSON.stringify(payment.comments),
    JSON.stringify(payment.timeline),
  ])
  await pool.query('insert into notifications (type, text, target, unread) values ($1, $2, $3, true)', [
    'comment',
    `${user.name} commented on ${payment.vendor}`,
    id,
  ])
  await pool.query('insert into audit_events (actor, action, ref, detail) values ($1, $2, $3, $4)', [user.name, 'Commented', id, text])
  return payment
}

async function markNotificationRead(id) {
  if (!pool) {
    memory.notifications = memory.notifications.map((notification) =>
      String(notification.id) === String(id) ? { ...notification, unread: false } : notification,
    )
    return
  }
  await pool.query('update notifications set unread = false where id = $1', [id])
}

function authenticate(request, response, next) {
  const token = request.headers.authorization?.replace('Bearer ', '')
  if (!token) return response.status(401).json({ message: 'Authentication required' })
  try {
    request.user = jwt.verify(token, jwtSecret)
    next()
  } catch {
    response.status(401).json({ message: 'Session expired' })
  }
}

function requireMd(request, response, next) {
  if (request.user.role !== 'md') return response.status(403).json({ message: 'MD approval access required' })
  next()
}

function publicUsers(rows) {
  return [
    { id: 'all', name: 'All Users', title: 'Consolidated treasury view', role: 'md' },
    ...rows.filter((user) => user.role !== 'md').map(publicUser),
  ]
}

function publicUser(user) {
  return { id: user.id, name: user.name, title: user.title, role: user.role }
}

function fromDbPayment(row) {
  return {
    id: row.id,
    vendor: row.vendor,
    contact: row.contact,
    userId: row.user_id,
    description: row.description,
    amount: Number(row.amount),
    paid: Number(row.paid),
    scheduledDate: row.scheduled_date,
    dueBucket: row.due_bucket,
    wallet: row.wallet,
    priority: row.priority,
    status: row.status,
    createdBy: row.created_by,
    attachment: row.attachment,
    createdAt: row.created_at_label,
    lastPayment: row.last_payment,
    previousPayments: Number(row.previous_payments),
    proof: row.proof,
    comments: Array.isArray(row.comments) ? row.comments : [],
    timeline: Array.isArray(row.timeline) ? row.timeline : [],
  }
}

function buildSeedAudit(payments) {
  return payments.flatMap((payment) => [
    { time: payment.createdAt, actor: payment.createdBy, action: 'Created bill', ref: payment.id, detail: payment.description },
    { time: payment.lastPayment, actor: payment.createdBy, action: 'Updated running balance', ref: payment.vendor, detail: `${payment.amount - payment.paid} outstanding` },
  ])
}
