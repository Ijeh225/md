import React, { useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  AlertTriangle,
  Archive,
  Bell,
  CalendarClock,
  Check,
  ChevronDown,
  CircleDollarSign,
  Clock,
  Coins,
  Download,
  FileText,
  History,
  LayoutDashboard,
  MessageSquare,
  Moon,
  MoreHorizontal,
  Pause,
  Printer,
  RefreshCw,
  Search,
  ShieldCheck,
  Sun,
  UserRound,
  Wallet,
  X,
} from 'lucide-react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import './styles.css'

const currency = new Intl.NumberFormat('en-NG', {
  style: 'currency',
  currency: 'NGN',
  maximumFractionDigits: 0,
})

const users = [
  { id: 'all', name: 'All Users', title: 'Consolidated treasury view' },
  { id: 'mr-a', name: 'Mr A', title: 'Operations payments' },
  { id: 'mr-b', name: 'Mr B', title: 'Procurement desk' },
  { id: 'mr-c', name: 'Mr C', title: 'Field logistics' },
]

const initialPayments = [
  {
    id: 'PAY-1001',
    vendor: 'Lucy Logistics',
    contact: '+234 802 100 4301',
    userId: 'mr-a',
    description: 'Loading and waybill handling for eastern route',
    amount: 100000,
    paid: 0,
    scheduledDate: 'Today',
    dueBucket: '0-7 days',
    wallet: 'Zenith Main Wallet',
    priority: 'High',
    status: 'Pending Approval',
    createdBy: 'Mr A',
    attachment: 'Invoice_Lucy_1001.pdf',
    createdAt: '2026-05-15 08:12',
    lastPayment: '2026-05-09',
    previousPayments: 420000,
    proof: 'Signed delivery note',
    comments: [
      { by: 'Mr A', text: 'Vendor is asking for settlement before dispatch.', at: '08:18' },
    ],
    timeline: ['Bill created by Mr A', 'Invoice attached', 'Moved to MD approval queue'],
  },
  {
    id: 'PAY-1002',
    vendor: 'Apex Diesel Supply',
    contact: '+234 805 311 6700',
    userId: 'mr-b',
    description: 'AGO supply for backup generators',
    amount: 850000,
    paid: 300000,
    scheduledDate: 'Today',
    dueBucket: '8-14 days',
    wallet: 'GTCO Treasury',
    priority: 'Critical',
    status: 'Approved Unpaid',
    createdBy: 'Mr B',
    attachment: 'Diesel_Supply_Proof.jpg',
    createdAt: '2026-05-15 07:24',
    lastPayment: '2026-05-13',
    previousPayments: 1900000,
    proof: 'Truck ticket and invoice',
    comments: [{ by: 'MD', text: 'Pay balance after wallet top-up.', at: '09:02' }],
    timeline: ['Bill created', 'Partial payment captured', 'MD approved remaining balance'],
  },
  {
    id: 'PAY-1003',
    vendor: 'Northline Engineering',
    contact: '+234 806 774 9124',
    userId: 'mr-c',
    description: 'Plant repair labor and replacement fittings',
    amount: 620000,
    paid: 0,
    scheduledDate: 'Tomorrow',
    dueBucket: '0-7 days',
    wallet: 'Access Project Account',
    priority: 'Medium',
    status: 'Scheduled',
    createdBy: 'Mr C',
    attachment: 'RepairEstimate.pdf',
    createdAt: '2026-05-14 17:44',
    lastPayment: '2026-05-05',
    previousPayments: 780000,
    proof: 'Engineer report',
    comments: [],
    timeline: ['Bill scheduled for tomorrow', 'Awaiting MD review'],
  },
  {
    id: 'PAY-1004',
    vendor: 'Prime Stationery',
    contact: '+234 809 112 4420',
    userId: 'mr-b',
    description: 'Office consumables and branded folders',
    amount: 240000,
    paid: 120000,
    scheduledDate: 'Tomorrow',
    dueBucket: '15-30 days',
    wallet: 'UBA Admin Wallet',
    priority: 'Low',
    status: 'Partial Payment',
    createdBy: 'Mr B',
    attachment: 'Stationery_PO.png',
    createdAt: '2026-05-13 12:08',
    lastPayment: '2026-05-14',
    previousPayments: 510000,
    proof: 'Purchase order',
    comments: [{ by: 'MD', text: 'Complete after reconciling delivery note.', at: 'Yesterday' }],
    timeline: ['Partial payment approved', 'Delivery proof requested'],
  },
  {
    id: 'PAY-1005',
    vendor: 'Stellar Haulage',
    contact: '+234 803 451 7761',
    userId: 'mr-a',
    description: 'Trailer movement and overnight security',
    amount: 480000,
    paid: 0,
    scheduledDate: 'Overdue',
    dueBucket: '30+ days overdue',
    wallet: 'Zenith Main Wallet',
    priority: 'Critical',
    status: 'Overdue',
    createdBy: 'Mr A',
    attachment: 'Haulage_bill.pdf',
    createdAt: '2026-04-22 10:31',
    lastPayment: '2026-04-19',
    previousPayments: 2100000,
    proof: 'Trip manifest',
    comments: [{ by: 'MD', text: 'Escalate and prioritize today.', at: '10:16' }],
    timeline: ['Payment missed scheduled date', 'Vendor called treasury', 'Escalated to MD'],
  },
  {
    id: 'PAY-1006',
    vendor: 'Crest Security Services',
    contact: '+234 807 002 2010',
    userId: 'mr-c',
    description: 'Facility night guard deployment',
    amount: 360000,
    paid: 360000,
    scheduledDate: 'Today',
    dueBucket: '0-7 days',
    wallet: 'Access Project Account',
    priority: 'Medium',
    status: 'Paid',
    createdBy: 'Mr C',
    attachment: 'Security_Timesheet.pdf',
    createdAt: '2026-05-15 06:40',
    lastPayment: '2026-05-15',
    previousPayments: 1440000,
    proof: 'Approved timesheet',
    comments: [{ by: 'MD', text: 'Approved.', at: '07:12' }],
    timeline: ['Bill created', 'MD approved', 'Payment completed by treasury'],
  },
]

const wallets = [
  { name: 'Zenith Main Wallet', balance: 2450000, limit: 1000000, userId: 'mr-a' },
  { name: 'GTCO Treasury', balance: 980000, limit: 1200000, userId: 'mr-b' },
  { name: 'Access Project Account', balance: 1740000, limit: 800000, userId: 'mr-c' },
  { name: 'UBA Admin Wallet', balance: 510000, limit: 600000, userId: 'mr-b' },
]

const baseNotifications = [
  { id: 1, type: 'comment', text: 'MD commented on Lucy Logistics payment', target: 'PAY-1001', unread: true },
  { id: 2, type: 'warning', text: 'GTCO Treasury wallet is below preferred float', target: 'wallet', unread: true },
  { id: 3, type: 'approval', text: 'Crest Security Services bill approved and paid', target: 'PAY-1006', unread: false },
  { id: 4, type: 'risk', text: 'Stellar Haulage is 23 days overdue', target: 'PAY-1005', unread: true },
]

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'today', label: 'Today', icon: CalendarClock },
  { id: 'tomorrow', label: 'Tomorrow', icon: Clock },
  { id: 'approvals', label: 'Approvals', icon: ShieldCheck },
  { id: 'liabilities', label: 'Liabilities', icon: Archive },
  { id: 'overdue', label: 'Overdue', icon: AlertTriangle },
  { id: 'vendors', label: 'Vendors', icon: UserRound },
  { id: 'reports', label: 'Reports', icon: FileText },
  { id: 'audit', label: 'Audit Trail', icon: History },
]

function App() {
  const [selectedUser, setSelectedUser] = useState('all')
  const [activePage, setActivePage] = useState('dashboard')
  const [payments, setPayments] = useState(initialPayments)
  const [notifications, setNotifications] = useState(baseNotifications)
  const [theme, setTheme] = useState('dark')
  const [query, setQuery] = useState('')
  const [selectedPaymentId, setSelectedPaymentId] = useState('PAY-1001')
  const [commentDraft, setCommentDraft] = useState('')
  const [notificationOpen, setNotificationOpen] = useState(false)
  const [soundEnabled, setSoundEnabled] = useState(true)

  const scopedPayments = useMemo(
    () => payments.filter((payment) => selectedUser === 'all' || payment.userId === selectedUser),
    [payments, selectedUser],
  )

  const filteredPayments = useMemo(() => {
    const search = query.trim().toLowerCase()
    if (!search) return scopedPayments
    return scopedPayments.filter((payment) =>
      [payment.vendor, payment.description, payment.status, payment.createdBy, payment.wallet, payment.priority]
        .join(' ')
        .toLowerCase()
        .includes(search),
    )
  }, [query, scopedPayments])

  const metrics = useMemo(() => buildMetrics(scopedPayments), [scopedPayments])
  const selectedPayment = payments.find((payment) => payment.id === selectedPaymentId) || payments[0]
  const unreadCount = notifications.filter((notification) => notification.unread).length

  const audit = useMemo(() => buildAudit(payments), [payments])

  function updatePayment(paymentId, action, overrides = {}) {
    setPayments((current) =>
      current.map((payment) => {
        if (payment.id !== paymentId) return payment
        const next = { ...payment, ...overrides }
        next.timeline = [`${action} by MD at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`, ...payment.timeline]
        return next
      }),
    )
    setNotifications((current) => [
      {
        id: Date.now(),
        type: 'approval',
        text: `${action} for ${payments.find((payment) => payment.id === paymentId)?.vendor}`,
        target: paymentId,
        unread: true,
      },
      ...current,
    ])
  }

  function addComment(paymentId, quickText) {
    const text = (quickText || commentDraft).trim()
    if (!text) return
    const stamped = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    setPayments((current) =>
      current.map((payment) =>
        payment.id === paymentId
          ? {
              ...payment,
              comments: [{ by: 'MD', text, at: stamped }, ...payment.comments],
              timeline: [`MD commented: ${text}`, ...payment.timeline],
            }
          : payment,
      ),
    )
    setNotifications((current) => [
      { id: Date.now(), type: 'comment', text: `MD commented on ${selectedPayment.vendor}`, target: paymentId, unread: true },
      ...current,
    ])
    setCommentDraft('')
  }

  function exportExcel(rows, name) {
    const data = rows.map(flattenPayment)
    const headers = Object.keys(data[0] || { Report: name })
    const body = [
      headers.join('\t'),
      ...data.map((row) => headers.map((header) => String(row[header] ?? '').replace(/\t/g, ' ')).join('\t')),
    ].join('\n')
    downloadBlob(body, `${name}.xls`, 'application/vnd.ms-excel')
  }

  function exportPdf(rows, name) {
    const table = rows.map((payment) => `
      <tr>
        <td>${escapeHtml(payment.vendor)}</td>
        <td>${escapeHtml(payment.description)}</td>
        <td>${currency.format(payment.amount)}</td>
        <td>${currency.format(payment.amount - payment.paid)}</td>
        <td>${escapeHtml(payment.scheduledDate)}</td>
        <td>${escapeHtml(payment.priority)}</td>
        <td>${escapeHtml(payment.status)}</td>
        <td>${escapeHtml(payment.createdBy)}</td>
      </tr>
    `).join('')
    const reportWindow = window.open('', '_blank', 'noopener,noreferrer')
    if (!reportWindow) return
    reportWindow.document.write(`
      <html>
        <head>
          <title>${escapeHtml(name)}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 28px; color: #111; }
            h1 { font-size: 24px; margin: 0 0 18px; }
            table { width: 100%; border-collapse: collapse; font-size: 12px; }
            th, td { border: 1px solid #d7dde2; padding: 8px; text-align: left; vertical-align: top; }
            th { background: #eef3f6; }
          </style>
        </head>
        <body>
          <h1>${escapeHtml(name)}</h1>
          <table>
            <thead><tr><th>Vendor</th><th>Description</th><th>Amount</th><th>Outstanding</th><th>Date</th><th>Priority</th><th>Status</th><th>Created By</th></tr></thead>
            <tbody>${table}</tbody>
          </table>
        </body>
      </html>
    `)
    reportWindow.document.close()
    reportWindow.print()
  }

  const pageProps = {
    payments: filteredPayments,
    allPayments: scopedPayments,
    selectedPayment,
    setSelectedPaymentId,
    updatePayment,
    addComment,
    commentDraft,
    setCommentDraft,
    exportExcel,
    exportPdf,
    audit,
  }

  return (
    <div className={`app ${theme}`}>
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      <main className="shell">
        <Topbar
          selectedUser={selectedUser}
          setSelectedUser={setSelectedUser}
          query={query}
          setQuery={setQuery}
          theme={theme}
          setTheme={setTheme}
          notifications={notifications}
          setNotifications={setNotifications}
          unreadCount={unreadCount}
          notificationOpen={notificationOpen}
          setNotificationOpen={setNotificationOpen}
          setActivePage={setActivePage}
          setSelectedPaymentId={setSelectedPaymentId}
          soundEnabled={soundEnabled}
          setSoundEnabled={setSoundEnabled}
        />
        {activePage === 'dashboard' && (
          <Dashboard
            metrics={metrics}
            payments={scopedPayments}
            selectedUser={selectedUser}
            setActivePage={setActivePage}
            wallets={wallets.filter((wallet) => selectedUser === 'all' || wallet.userId === selectedUser)}
          />
        )}
        {activePage === 'today' && <PaymentsPage title="Total Scheduled Payments Today" mode="Today" {...pageProps} />}
        {activePage === 'tomorrow' && <PaymentsPage title="Tomorrow's Scheduled Payments" mode="Tomorrow" tomorrow {...pageProps} />}
        {activePage === 'approvals' && <PaymentsPage title="Pending Approval Bills" mode="Pending Approval" approval {...pageProps} />}
        {activePage === 'liabilities' && <LiabilitiesPage payments={filteredPayments} exportExcel={exportExcel} exportPdf={exportPdf} />}
        {activePage === 'overdue' && <OverduePage {...pageProps} />}
        {activePage === 'vendors' && <VendorsPage payments={filteredPayments} />}
        {activePage === 'reports' && <ReportsPage payments={filteredPayments} audit={audit} exportExcel={exportExcel} exportPdf={exportPdf} />}
        {activePage === 'audit' && <AuditPage audit={audit} />}
      </main>
    </div>
  )
}

function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><Coins size={22} /></div>
        <div>
          <strong>MD Treasury</strong>
          <span>Private control system</span>
        </div>
      </div>
      <nav>
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <button key={item.id} className={activePage === item.id ? 'active' : ''} onClick={() => setActivePage(item.id)}>
              <Icon size={18} />
              {item.label}
            </button>
          )
        })}
      </nav>
      <div className="secure-card">
        <ShieldCheck size={22} />
        <strong>Executive access</strong>
        <span>MD and selected treasury/payment assistants only.</span>
      </div>
    </aside>
  )
}

function Topbar(props) {
  const {
    selectedUser,
    setSelectedUser,
    query,
    setQuery,
    theme,
    setTheme,
    notifications,
    setNotifications,
    unreadCount,
    notificationOpen,
    setNotificationOpen,
    setActivePage,
    setSelectedPaymentId,
    soundEnabled,
    setSoundEnabled,
  } = props

  function openNotification(notification) {
    setNotifications((current) => current.map((item) => (item.id === notification.id ? { ...item, unread: false } : item)))
    if (notification.target?.startsWith('PAY-')) {
      setSelectedPaymentId(notification.target)
      setActivePage('approvals')
    }
    setNotificationOpen(false)
  }

  return (
    <header className="topbar">
      <div className="user-switch">
        <select value={selectedUser} onChange={(event) => setSelectedUser(event.target.value)} aria-label="Switch user workspace">
          {users.map((user) => (
            <option key={user.id} value={user.id}>{user.name}</option>
          ))}
        </select>
        <ChevronDown size={16} />
      </div>
      <label className="search">
        <Search size={18} />
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search vendors, bills, wallets, approvals..." />
      </label>
      <button className="icon-button" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} title="Toggle theme">
        {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
      </button>
      <div className="notification-zone">
        <button className="icon-button bell" onClick={() => setNotificationOpen(!notificationOpen)} title="Notifications">
          <Bell size={18} />
          {unreadCount > 0 && <span>{unreadCount}</span>}
        </button>
        {notificationOpen && (
          <div className="notification-menu">
            <div className="notification-head">
              <strong>Notifications</strong>
              <label>
                Sound
                <input type="checkbox" checked={soundEnabled} onChange={(event) => setSoundEnabled(event.target.checked)} />
              </label>
            </div>
            {notifications.map((notification) => (
              <button key={notification.id} className={notification.unread ? 'unread' : ''} onClick={() => openNotification(notification)}>
                <span className={`dot ${notification.type}`} />
                {notification.text}
              </button>
            ))}
          </div>
        )}
      </div>
    </header>
  )
}

function Dashboard({ metrics, payments, selectedUser, setActivePage, wallets }) {
  const cards = [
    ['Total Scheduled Payments Today', metrics.todayTotal, 'today', CalendarClock],
    ["Tomorrow's Scheduled Payments", metrics.tomorrowTotal, 'tomorrow', Clock],
    ['Pending Approval Bills', metrics.pendingTotal, 'approvals', ShieldCheck],
    ['Approved but Unpaid Bills', metrics.approvedUnpaidTotal, 'approvals', Pause],
    ['Total Outstanding Liabilities', metrics.outstandingTotal, 'liabilities', Archive],
    ['Overdue Bills', metrics.overdueTotal, 'overdue', AlertTriangle],
    ['Wallet Balances', wallets.reduce((sum, wallet) => sum + wallet.balance, 0), 'liabilities', Wallet],
    ['Total Paid Today', metrics.paidToday, 'today', Check],
    ['Partial Payments', metrics.partialTotal, 'approvals', CircleDollarSign],
    ['Recent Transactions', metrics.recentTotal, 'reports', RefreshCw],
    ['Notifications', metrics.notificationSignal, 'audit', Bell],
    ['User Activity Summary', metrics.activityCount, 'audit', History],
  ]

  const selected = users.find((user) => user.id === selectedUser)
  const flow = [
    { name: 'Paid', value: metrics.paidToday },
    { name: 'Pending', value: metrics.pendingTotal },
    { name: 'Outstanding', value: metrics.outstandingTotal },
    { name: 'Overdue', value: metrics.overdueTotal },
  ]
  const byUser = groupByUser(payments)

  return (
    <section className="page">
      <div className="hero">
        <div>
          <span className="eyebrow">Executive command center</span>
          <h1>{selected?.name} Treasury Workspace</h1>
          <p>{selected?.title}. Smart approvals, running vendor balances, wallet visibility, and audit-ready activity in one private console.</p>
        </div>
        <div className="hero-stat">
          <span>Outstanding exposure</span>
          <strong>{currency.format(metrics.outstandingTotal)}</strong>
          <small>{metrics.overdueCount} overdue item{metrics.overdueCount === 1 ? '' : 's'} require attention</small>
        </div>
      </div>
      <div className="summary-grid">
        {cards.map((card) => {
          const [label, value, page, CardIcon] = card
          return (
            <button key={label} className="summary-card" onClick={() => setActivePage(page)}>
              <div className="card-icon"><CardIcon size={20} /></div>
              <span>{label}</span>
              <strong>{typeof value === 'number' && value > 999 ? currency.format(value) : value}</strong>
              <small>Open details</small>
            </button>
          )
        })}
      </div>
      <div className="dashboard-panels">
        <Panel title="Payment Flow">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={flow}>
              <defs>
                <linearGradient id="flow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#51d6ff" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#51d6ff" stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="name" stroke="var(--muted)" />
              <YAxis stroke="var(--muted)" tickFormatter={(value) => `${value / 1000}k`} />
              <Tooltip formatter={(value) => currency.format(value)} />
              <Area type="monotone" dataKey="value" stroke="#51d6ff" fill="url(#flow)" />
            </AreaChart>
          </ResponsiveContainer>
        </Panel>
        <Panel title="Liability Per User">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={byUser}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--grid)" />
              <XAxis dataKey="name" stroke="var(--muted)" />
              <YAxis stroke="var(--muted)" tickFormatter={(value) => `${value / 1000}k`} />
              <Tooltip formatter={(value) => currency.format(value)} />
              <Bar dataKey="outstanding" radius={[8, 8, 0, 0]} fill="#b9ff66" />
            </BarChart>
          </ResponsiveContainer>
        </Panel>
      </div>
    </section>
  )
}

function PaymentsPage(props) {
  const rows = props.payments
    .filter((payment) => (props.mode === 'Pending Approval' ? payment.status === 'Pending Approval' : payment.scheduledDate === props.mode))
    .sort((a, b) => priorityRank(b.priority) - priorityRank(a.priority) || b.amount - a.amount)

  return (
    <section className="page two-column">
      <div>
        <PageHead title={props.title} rows={rows} exportExcel={props.exportExcel} exportPdf={props.exportPdf} />
        <div className="group-strip">
          <Badge>Grouped by user</Badge>
          <Badge>Grouped by vendor</Badge>
          <Badge>Grouped by priority</Badge>
          <Badge>Grouped by due date</Badge>
          {props.tomorrow && <Badge>Approve ahead</Badge>}
          {props.approval && <Badge>Supporting proof</Badge>}
        </div>
        <SmartTable rows={rows} onSelect={props.setSelectedPaymentId} selectedId={props.selectedPayment?.id} updatePayment={props.updatePayment} />
      </div>
      <PaymentInspector {...props} payment={props.selectedPayment} />
    </section>
  )
}

function SmartTable({ rows, onSelect, selectedId, updatePayment }) {
  return (
    <div className="table-card">
      <table>
        <thead>
          <tr>
            <th>Vendor / Beneficiary</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Outstanding</th>
            <th>Schedule</th>
            <th>Wallet</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((payment) => (
            <tr key={payment.id} className={selectedId === payment.id ? 'selected-row' : ''} onClick={() => onSelect(payment.id)}>
              <td><strong>{payment.vendor}</strong><span>{payment.createdBy}</span></td>
              <td>{payment.description}<span className="attachment">{payment.attachment}</span></td>
              <td>{currency.format(payment.amount)}</td>
              <td>{currency.format(payment.amount - payment.paid)}</td>
              <td>{payment.scheduledDate}</td>
              <td>{payment.wallet}</td>
              <td><StatusBadge value={payment.priority} /></td>
              <td><StatusBadge value={payment.status} /></td>
              <td>{payment.createdAt}</td>
              <td>
                <div className="row-actions">
                  <button onClick={(event) => { event.stopPropagation(); updatePayment(payment.id, 'Approved', { status: 'Approved Unpaid' }) }} title="Approve"><Check size={15} /></button>
                  <button onClick={(event) => { event.stopPropagation(); updatePayment(payment.id, 'Rejected', { status: 'Rejected' }) }} title="Reject"><X size={15} /></button>
                  <button onClick={(event) => { event.stopPropagation(); updatePayment(payment.id, 'Held', { status: 'On Hold' }) }} title="Hold"><Pause size={15} /></button>
                  <button onClick={(event) => { event.stopPropagation(); updatePayment(payment.id, 'Partial approval', { status: 'Partial Payment', paid: Math.max(payment.paid, Math.floor(payment.amount * 0.5)) }) }} title="Partial approve"><CircleDollarSign size={15} /></button>
                  <button onClick={(event) => event.stopPropagation()} title="Comment"><MessageSquare size={15} /></button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function PaymentInspector({ payment, commentDraft, setCommentDraft, addComment, updatePayment }) {
  const quick = ['Pay ₦50,000 first', 'Hold till tomorrow', 'Confirm invoice', 'Use Zenith wallet', 'Why is this amount high?', 'Approved', 'Reduce amount']
  if (!payment) return <Panel title="Payment Details"><p>No payment selected.</p></Panel>
  return (
    <aside className="inspector">
      <Panel title={payment.vendor}>
        <div className="inspector-total">
          <span>Outstanding balance</span>
          <strong>{currency.format(payment.amount - payment.paid)}</strong>
        </div>
        <div className="detail-list">
          <span>Description<b>{payment.description}</b></span>
          <span>Wallet<b>{payment.wallet}</b></span>
          <span>Proof<b>{payment.proof}</b></span>
          <span>Previous payments<b>{currency.format(payment.previousPayments)}</b></span>
          <span>Attachment preview<b>{payment.attachment}</b></span>
        </div>
        <div className="action-grid">
          <button onClick={() => updatePayment(payment.id, 'Approved', { status: 'Approved Unpaid' })}><Check size={16} />Approve</button>
          <button onClick={() => updatePayment(payment.id, 'Rejected', { status: 'Rejected' })}><X size={16} />Reject</button>
          <button onClick={() => updatePayment(payment.id, 'Held', { status: 'On Hold' })}><Pause size={16} />Hold</button>
          <button onClick={() => updatePayment(payment.id, 'Moved to tomorrow', { scheduledDate: 'Tomorrow' })}><Clock size={16} />Move date</button>
        </div>
      </Panel>
      <Panel title="MD Comment Thread">
        <div className="quick-comments">
          {quick.map((item) => <button key={item} onClick={() => addComment(payment.id, item)}>{item}</button>)}
        </div>
        <textarea value={commentDraft} onChange={(event) => setCommentDraft(event.target.value)} placeholder="Type MD comment..." />
        <button className="primary" onClick={() => addComment(payment.id)}><MessageSquare size={16} />Send comment</button>
        <div className="thread">
          {payment.comments.map((comment, index) => (
            <div key={`${comment.at}-${index}`}>
              <strong>{comment.by}</strong>
              <p>{comment.text}</p>
              <span>{comment.at}</span>
            </div>
          ))}
        </div>
      </Panel>
      <Panel title="Activity Timeline">
        <div className="timeline">
          {payment.timeline.map((event, index) => <span key={index}>{event}</span>)}
        </div>
      </Panel>
    </aside>
  )
}

function LiabilitiesPage({ payments, exportExcel, exportPdf }) {
  const unpaid = payments.filter((payment) => payment.amount - payment.paid > 0)
  const aging = ['0-7 days', '8-14 days', '15-30 days', '30+ days overdue'].map((bucket) => ({
    name: bucket,
    value: unpaid.filter((payment) => payment.dueBucket === bucket).reduce((sum, payment) => sum + payment.amount - payment.paid, 0),
  }))
  return (
    <section className="page">
      <PageHead title="Total Outstanding Liabilities" rows={unpaid} exportExcel={exportExcel} exportPdf={exportPdf} />
      <div className="dashboard-panels">
        <Panel title="Aging of Liabilities">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={aging} dataKey="value" nameKey="name" innerRadius={70} outerRadius={105} paddingAngle={4}>
                {aging.map((_, index) => <Cell key={index} fill={['#51d6ff', '#b9ff66', '#ffd166', '#ff6b6b'][index]} />)}
              </Pie>
              <Tooltip formatter={(value) => currency.format(value)} />
            </PieChart>
          </ResponsiveContainer>
        </Panel>
        <Panel title="Liability Ledger">
          <Ledger rows={unpaid} />
        </Panel>
      </div>
    </section>
  )
}

function OverduePage(props) {
  const overdue = props.payments.filter((payment) => payment.status === 'Overdue' || payment.scheduledDate === 'Overdue')
  return (
    <section className="page">
      <PageHead title="Overdue Bills" rows={overdue} exportExcel={props.exportExcel} exportPdf={props.exportPdf} />
      <SmartTable rows={overdue} onSelect={props.setSelectedPaymentId} selectedId={props.selectedPayment?.id} updatePayment={props.updatePayment} />
      <div className="overdue-actions">
        {overdue.map((payment) => (
          <Panel key={payment.id} title={`${payment.vendor} escalation`}>
            <p>{payment.vendor} has an unpaid balance of {currency.format(payment.amount - payment.paid)}. Last comment: {payment.comments[0]?.text || 'No comment yet'}.</p>
            <div className="action-grid">
              <button onClick={() => props.updatePayment(payment.id, 'Escalated', { priority: 'Critical' })}>Escalate</button>
              <button onClick={() => props.updatePayment(payment.id, 'Rescheduled', { scheduledDate: 'Today' })}>Reschedule</button>
              <button onClick={() => props.updatePayment(payment.id, 'Prioritized', { priority: 'Critical' })}>Prioritize</button>
            </div>
          </Panel>
        ))}
      </div>
    </section>
  )
}

function VendorsPage({ payments }) {
  const vendors = Object.values(payments.reduce((acc, payment) => {
    acc[payment.vendor] ||= { vendor: payment.vendor, total: 0, paid: 0, jobs: 0, user: payment.createdBy, contact: payment.contact, history: [] }
    acc[payment.vendor].total += payment.amount
    acc[payment.vendor].paid += payment.paid
    acc[payment.vendor].jobs += 1
    acc[payment.vendor].history.push(payment)
    return acc
  }, {}))
  return (
    <section className="page">
      <PageHead title="Beneficiary / Vendor Running Balances" rows={payments} />
      <div className="vendor-grid">
        {vendors.map((vendor) => (
          <Panel key={vendor.vendor} title={vendor.vendor}>
            <div className="vendor-balance">
              <span>Total bills<strong>{currency.format(vendor.total)}</strong></span>
              <span>Total paid<strong>{currency.format(vendor.paid)}</strong></span>
              <span>Outstanding<strong>{currency.format(vendor.total - vendor.paid)}</strong></span>
            </div>
            <p>{vendor.jobs} job history item{vendor.jobs === 1 ? '' : 's'} created by {vendor.user}. Contact: {vendor.contact}</p>
            <div className="timeline compact">
              {vendor.history.map((item) => <span key={item.id}>{item.description} - {currency.format(item.amount - item.paid)} outstanding</span>)}
            </div>
          </Panel>
        ))}
      </div>
    </section>
  )
}

function ReportsPage({ payments, audit, exportExcel, exportPdf }) {
  const reports = [
    'Daily payment report',
    'Scheduled payments',
    'Outstanding liabilities',
    'Vendor statement',
    'Wallet statement',
    'User activity',
    'Partial payments',
    'Approval logs',
    'Audit trail',
  ]
  return (
    <section className="page">
      <PageHead title="Reports & Exports" rows={payments} exportExcel={exportExcel} exportPdf={exportPdf} />
      <div className="report-grid">
        {reports.map((report) => (
          <div className="report-card" key={report}>
            <FileText size={22} />
            <strong>{report}</strong>
            <div>
              <button onClick={() => exportExcel(payments, report)}><Download size={15} />Excel</button>
              <button onClick={() => exportPdf(payments, report)}><FileText size={15} />PDF</button>
              <button onClick={() => window.print()}><Printer size={15} />Print</button>
            </div>
          </div>
        ))}
      </div>
      <AuditPage audit={audit.slice(0, 6)} embedded />
    </section>
  )
}

function AuditPage({ audit, embedded }) {
  return (
    <section className={embedded ? '' : 'page'}>
      {!embedded && <PageHead title="Audit Trail" rows={[]} />}
      <div className="table-card">
        <table>
          <thead>
            <tr><th>Time</th><th>Actor</th><th>Action</th><th>Reference</th><th>Detail</th></tr>
          </thead>
          <tbody>
            {audit.map((entry, index) => (
              <tr key={index}>
                <td>{entry.time}</td>
                <td>{entry.actor}</td>
                <td>{entry.action}</td>
                <td>{entry.ref}</td>
                <td>{entry.detail}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function PageHead({ title, rows, exportExcel, exportPdf }) {
  return (
    <div className="page-head">
      <div>
        <span className="eyebrow">Treasury detail page</span>
        <h2>{title}</h2>
      </div>
      <div className="head-actions">
        {exportExcel && <button onClick={() => exportExcel(rows, title)}><Download size={16} />Excel</button>}
        {exportPdf && <button onClick={() => exportPdf(rows, title)}><FileText size={16} />PDF</button>}
        <button onClick={() => window.print()}><Printer size={16} />Print</button>
      </div>
    </div>
  )
}

function Panel({ title, children }) {
  return (
    <section className="panel">
      <div className="panel-title">
        <h3>{title}</h3>
        <MoreHorizontal size={18} />
      </div>
      {children}
    </section>
  )
}

function Badge({ children }) {
  return <span className="badge">{children}</span>
}

function StatusBadge({ value }) {
  return <span className={`status ${value.toLowerCase().replaceAll(' ', '-')}`}>{value}</span>
}

function Ledger({ rows }) {
  return (
    <div className="ledger">
      {rows.map((payment) => (
        <div key={payment.id}>
          <strong>{payment.vendor}</strong>
          <span>{payment.createdBy} • {payment.dueBucket} • Last payment {payment.lastPayment}</span>
          <b>{currency.format(payment.amount - payment.paid)}</b>
        </div>
      ))}
    </div>
  )
}

function buildMetrics(payments) {
  return {
    todayTotal: sum(payments.filter((payment) => payment.scheduledDate === 'Today'), 'amount'),
    tomorrowTotal: sum(payments.filter((payment) => payment.scheduledDate === 'Tomorrow'), 'amount'),
    pendingTotal: sum(payments.filter((payment) => payment.status === 'Pending Approval'), 'amount'),
    approvedUnpaidTotal: sum(payments.filter((payment) => payment.status === 'Approved Unpaid'), 'amount'),
    outstandingTotal: payments.reduce((total, payment) => total + Math.max(payment.amount - payment.paid, 0), 0),
    overdueTotal: sum(payments.filter((payment) => payment.status === 'Overdue'), 'amount'),
    paidToday: sum(payments.filter((payment) => payment.status === 'Paid' && payment.scheduledDate === 'Today'), 'paid'),
    partialTotal: sum(payments.filter((payment) => payment.status === 'Partial Payment'), 'paid'),
    recentTotal: payments.length,
    notificationSignal: payments.filter((payment) => payment.comments.length > 0).length,
    activityCount: payments.reduce((total, payment) => total + payment.timeline.length, 0),
    overdueCount: payments.filter((payment) => payment.status === 'Overdue').length,
  }
}

function sum(rows, key) {
  return rows.reduce((total, row) => total + row[key], 0)
}

function priorityRank(priority) {
  return { Low: 1, Medium: 2, High: 3, Critical: 4 }[priority] || 0
}

function groupByUser(payments) {
  return users
    .filter((user) => user.id !== 'all')
    .map((user) => ({
      name: user.name,
      outstanding: payments
        .filter((payment) => payment.userId === user.id)
        .reduce((total, payment) => total + Math.max(payment.amount - payment.paid, 0), 0),
    }))
}

function flattenPayment(payment) {
  return {
    Vendor: payment.vendor,
    Description: payment.description,
    Amount: payment.amount,
    Paid: payment.paid,
    Outstanding: payment.amount - payment.paid,
    ScheduledDate: payment.scheduledDate,
    Wallet: payment.wallet,
    Priority: payment.priority,
    Status: payment.status,
    CreatedBy: payment.createdBy,
    Attachment: payment.attachment,
    CreatedAt: payment.createdAt,
  }
}

function downloadBlob(content, filename, type) {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function buildAudit(payments) {
  return payments.flatMap((payment) => [
    { time: payment.createdAt, actor: payment.createdBy, action: 'Created bill', ref: payment.id, detail: payment.description },
    { time: payment.lastPayment, actor: payment.createdBy, action: 'Updated running balance', ref: payment.vendor, detail: `${currency.format(payment.amount - payment.paid)} outstanding` },
    ...payment.comments.map((comment) => ({ time: comment.at, actor: comment.by, action: 'Commented', ref: payment.id, detail: comment.text })),
    ...payment.timeline.slice(0, 2).map((event) => ({ time: 'Recent', actor: event.includes('MD') ? 'MD' : payment.createdBy, action: 'Workflow event', ref: payment.id, detail: event })),
  ])
}

createRoot(document.getElementById('root')).render(<App />)
