# MD Treasury Command

Private executive finance control dashboard for the MD and selected treasury/payment assistants. The app is now a full-stack production foundation with a Node/Express API, JWT login, persistent approval workflows, and Render Postgres storage.

## Features

- Clickable MD dashboard summary cards that open detailed finance sections
- Smooth MD user workspace switching for All Users, Mr A, Mr B, and Mr C
- Scheduled payment pages for today and tomorrow
- Approval workflow with approve, reject, hold, partial approve, comments, and timelines
- Vendor running balances with total bills, paid amount, outstanding liabilities, job history, and activity history
- Overdue bill management with escalation, rescheduling, prioritization, and comments
- Real-time-style notifications with unread count, dropdown, target navigation, and sound toggle
- Audit trail for created bills, workflow events, comments, and balance updates
- Excel-compatible report export, printable/PDF reports, and print support
- Dark/light mode, responsive layout, smart tables, charts, badges, sticky filters, and search
- JWT-protected backend API
- Render Postgres persistence for payments, comments, notifications, wallets, users, and audit logs
- Automatic database schema creation and first-run seed data

## Local Development

```bash
npm install
npm run dev
```

Open `http://localhost:5173` for frontend-only development.

For the production server flow:

```bash
npm run build
npm start
```

Open `http://localhost:3000`.

Local fallback login:

```text
User: Managing Director
Password: ChangeMe123!
```

## Build

```bash
npm run build
```

## Render Deployment

This repo includes `render.yaml` for a Render Node web service and managed Postgres database.

Use this Blueprint URL after the repo is pushed:

```text
https://dashboard.render.com/blueprint/new?repo=https://github.com/Ijeh225/MD-APP
```

Render will run:

```bash
npm ci && npm run build
```

Then start:

```bash
npm start
```

Set `MD_INITIAL_PASSWORD` when Render asks for secrets. The app generates `JWT_SECRET` automatically and attaches `DATABASE_URL` from the Blueprint database.

First production login:

```text
User: Managing Director
Password: the value you set for MD_INITIAL_PASSWORD
```
