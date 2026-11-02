# TaskFlow — AI Agent Context Document

> **Purpose**: Single source of truth for any AI agent (or human) working on this codebase.
> Keep this updated as the project evolves.

---

## 1. Project Overview

**TaskFlow** — A calendar/task-management web app in early proof-of-concept stage.

- **Goal**: Create, store, read, update, delete tasks with dates/times
- **Architecture**: Microservices (3 services + reverse proxy + DB)
- **Stack**: Python/FastAPI, Node/Express, PostgreSQL, Docker, Traefik
- **Author**: Solo learner project (akbanana7)
- **Repo**: https://github.com/akbanana7/TaskFlow

---

## 2. Service Map

| Service | Port (internal) | Tech | Role |
|---------|-----------------|------|------|
| **front** | 8080 | Node 22 + Express 5 | Static file server (HTML/JS/CSS) |
| **backendPy (analytics)** | 8000 | Python 3.14 + FastAPI + psycopg | Task CRUD API → PostgreSQL |
| **auth** | 8090 | Python 3.14 + FastAPI | Placeholder — only CORS + skeleton |
| **database** | 5432 | PostgreSQL 18 | Persistent storage (`TaskFlow` DB) |
| **traefik** | 80 (HTTP), 8080 (dashboard) | Traefik 3.7 | Reverse proxy, routing, TLS termination |

**External access**: Everything routed through Traefik on **port 80**.
- Frontend → `http://<host>/`
- Backend API → `http://<host>/api/...` (strip prefix middleware)

---

## 3. Directory Structure

```
.
├── analytics/           # FastAPI task CRUD service
│   ├── app.py           # Main entrypoint (READ THIS)
│   ├── Dockerfile
│   └── requirements.txt
├── auth/                # Auth service (stub)
│   └── auth.py
├── front/               # Express static frontend
│   ├── server.js
│   ├── Dockerfile
│   ├── package.json
│   └── public/
│       ├── index.html
│       ├── formHandler.js   # POST /api/add/
│       ├── readHandler.js   # GET  /api/find/
│       └── style.css
├── fileServer/          # Empty (reserved)
├── .github/workflows/   # CI: docker compose build + up + healthcheck
├── docker-compose.yml   # Full stack orchestration
├── README.md
├── .gitignore
└── context.md           # ← YOU ARE HERE
```

---

## 4. Key Files — Deep Dive

### 4.1 `analytics/app.py` — **Primary Backend**
- **Endpoints**:
  - `GET  /init/` — Drop & recreate `main` table (dev only)
  - `POST /add/`  — Insert task (validated via Pydantic `task` model)
  - `GET  /find/` — Query by `user` + `taskName` (returns ISO-formatted arrays)
  - `GET  /update` — **BROKEN** (GET with body, SQL injection, unbound vars)
- **Table Schema** (`main`):
  ```sql
  "user" varchar(255),
  "taskName" varchar(255),
  "taskDesc" text,
  timeStart time,
  timeEnd time,
  timezone int,       -- hardcoded "0" (UTC)
  dateStart date,
  dateEnd date
  ```
- **Connection**: `getDbConnection()` — auto-creates DB if missing, uses `DB_PASS`, `PGHOST` env vars
- **Known Issues**:
  - `/find/` uses f-string SQL → **SQL injection**
  - `/update` is fundamentally broken (wrong method, variable order, string interpolation)
  - No authentication / user isolation
  - Timezone hardcoded
  - No DELETE endpoint

### 4.2 `front/public/formHandler.js`
- Hardcoded `user = "temp"`
- `POST /api/add/` with JSON body matching `task` model
- No error handling / user feedback

### 4.3 `front/public/readHandler.js`
- Hardcoded `user = "temp"`
- `GET /api/find/?user=...&taskName=...`
- Renders results into `#taskDetails` div (skips first column = user)

### 4.4 `docker-compose.yml`
- **Networking**: All services on default Docker network; Traefik labels handle routing
- **DB Healthcheck**: `pg_isready` — backend waits for `condition: service_healthy`
- **Traefik Strip Prefix**: `/api` → `/` for backendPy
- **Volumes**: `./prod/db` → PG data (bind mount)
- **Ports**: 80 (web), 8000 (Traefik alt), 8080 (dashboard localhost only)

### 4.5 `.github/workflows/deploy-test.yaml`
- Runs on every push/PR
- `docker compose config` → `build --no-cache` → `up -d` → wait for DB healthy → `down -v`

### 4.6 `.github/workflows/test.yaml` — **Test Suite**
- **Backend Tests** (`backendTests`): Pytest + httpx against real Postgres service
- **Frontend Tests** (`frontendTests`): Jest + ESLint (placeholder — no local tests yet)
- **E2E Tests** (`e2eTests`): Full docker-compose stack, API contract tests
- **Security Scan** (`securityScan`): Trivy vuln scan + Gitleaks secret detection
- **Summary Gate** (`testSummary`): All jobs must pass

---

## 5. Environment Variables

| Var | Used By | Example |
|-----|---------|---------|
| `DB_PASS` | analytics, database | `main123` |
| `PGHOST` | analytics | `database` (Docker service name) |
| `POSTGRES_DB` | database | `TaskFlow` |
| `POSTGRES_PASSWORD` | database | `main123` |

> **Never commit real secrets.** `.gitignore` excludes `.env`, `secrets/`, `postgres_password.txt`.

---

## 6. Development Workflow

### Start Everything (Docker Compose)
```bash
docker compose down       # clean slate
docker compose build      # build images
docker compose up         # run (logs in foreground)
# or: docker compose up -d  # detached
```

### Access Points
- Frontend: `http://localhost/`
- Backend API: `http://localhost/api/...`
- Traefik Dashboard: `http://localhost:8080/` (localhost only)

### Individual Service Dev
```bash
# Backend (analytics)
cd analytics && python app.py        # runs on 8000 with reload

# Frontend
cd front && npm start                # runs on 8080
```
> Requires local Postgres + env vars if not using compose.

---

## 7. CI/CD Pipeline

**GitHub Actions** (`.github/workflows/deploy-test.yaml`):
1. Checkout
2. `docker compose config -q` (validate)
3. `docker compose build --no-cache`
4. `docker compose up -d`
5. Poll DB healthcheck (30 × 2s)
6. Cleanup (`down -v`) always runs

**Test Suite** (`.github/workflows/test.yaml`):
1. Backend unit/integration tests (pytest + Postgres service)
2. Frontend lint + unit tests (Jest)
3. E2E integration tests (full stack via docker-compose)
4. Security scanning (Trivy + Gitleaks)
5. Summary gate — all must pass

No deploy step yet — only validation.

---

## 8. Current State & TODOs (Priority Order)

### 🔴 Critical (Blockers)
- [ ] **Fix `/update` endpoint** — change to `PUT/PATCH`, fix SQL, bind params, add auth check
- [ ] **Fix SQL injection in `/find/`** — use parameterized queries
- [ ] **Add DELETE endpoint** — `DELETE /delete/?user=...&taskName=...`
- [ ] **Implement Authentication** — replace hardcoded `"temp"` user

### 🟠 High
- [ ] Add proper error handling & HTTP status codes in frontend JS
- [ ] Input validation on frontend (required fields, date logic)
- [ ] Timezone support (store IANA tz, convert on read)
- [ ] Pagination / listing endpoint (`GET /list/?user=...`)
- [ ] Unique constraint on (`user`, `taskName`) or add UUID PK

### 🟡 Medium
- [ ] Migrate to Alembic for schema migrations
- [ ] Add indexes on `user`, `taskName`, `dateStart`
- [ ] Unit/integration tests (pytest + httpx for backend, Jest for frontend)
- [ ] OpenAPI/Swagger docs (FastAPI auto-generates at `/docs`)
- [ ] Frontend: show loading states, toast notifications

### 🟢 Low / Nice-to-have
- [ ] Recurring tasks
- [ ] Task categories / tags
- [ ] Calendar view (FullCalendar.js or similar)
- [ ] HTTPS via Traefik + Let's Encrypt
- [ ] Kubernetes manifests (`k8s/` dir exists but empty)

---

## 9. Conventions & Patterns

| Area | Convention |
|------|------------|
| **Python** | Type hints, Pydantic models, `async def` for I/O |
| **SQL** | Parameterized queries (`%s` placeholders), double-quote identifiers |
| **JS** | Vanilla ES6, `fetch` API, `DOMContentLoaded` guard |
| **Docker** | Multi-stage not yet used; slim base images |
| **Git** | Main branch only; CI runs on all pushes |
| **Naming** | camelCase (Python), camelCase (JS), kebab-case (URLs) |

---

## 10. Common Commands Cheatsheet

```bash
# View logs
docker compose logs -f backendPy
docker compose logs -f front

# Shell into container
docker compose exec backendPy bash
docker compose exec database psql -U postgres -d TaskFlow

# Reset DB (dev only)
curl -X GET "http://localhost/api/init/"

# Test API manually
curl -X POST http://localhost/api/add/ \
  -H "Content-Type: application/json" \
  -d '{"user":"temp","taskName":"Test","taskDesc":"Desc","dateStart":"2025-01-15","dateEnd":"2025-01-15","timeStart":"09:00","timeEnd":"10:00"}'

curl "http://localhost/api/find/?user=temp&taskName=Test"
```

---

## 11. Gotchas & Tribal Knowledge

1. **Traefik strips `/api`** — backend routes are defined as `/add/`, `/find/` (no `/api` prefix in code)
2. **Frontend calls `/api/...`** — works because Traefik adds the prefix back
3. **DB host is `database`** inside Docker network; `localhost` won't work from containers
4. **Python 3.14** — bleeding edge; may have ecosystem issues (use 3.12/3.13 for stability)
5. **Express 5** — still in beta; middleware signatures may differ from v4
6. **No migrations** — schema changes require manual `DROP TABLE` + `CREATE` or `/init/`
7. **CORS** — backend allows `*`; auth service restricts to localhost regex
8. **Volumes** — `./prod/db` bind mount persists data across `compose down` (unless `-v`)

---

## 12. Quick-Start for New Agents

1. Read this file + `README.md`
2. `docker compose up` → verify frontend loads at `http://localhost/`
3. Open `analytics/app.py` — understand the 4 endpoints & bugs
4. Pick a TODO from Section 8
5. Write code → test manually → run CI locally (`docker compose build && docker compose up -d`)
6. Update this `context.md` with changes

---

*Last updated: 2025-01-15 (auto-generated by AI agent)*
*Update this file whenever you change architecture, add endpoints, modify schema, or fix critical bugs.*