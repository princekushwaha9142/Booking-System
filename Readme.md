# Booking System API

![CI](https://github.com/princekushwaha9142/Booking-System/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/princekushwaha9142/Booking-System/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)
![Celery](https://img.shields.io/badge/Celery-5.3.6-37814A?logo=celery)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Alembic](https://img.shields.io/badge/Alembic-1.13.1-blue)
![Pytest](https://img.shields.io/badge/Tests-12%2F12%20Passed-brightgreen?logo=pytest)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?logo=jsonwebtokens)
![Resend](https://img.shields.io/badge/Email-Resend-000000?logo=mail)
![License](https://img.shields.io/badge/License-MIT-green)

🌐 **Live API:** https://booking-system-skjo.onrender.com  
📖 **Docs:** https://booking-system-skjo.onrender.com/docs

A production-ready REST API for hotel and flight bookings built with FastAPI, PostgreSQL, Redis, Celery, and JWT Authentication.

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.111.0 | Web framework |
| **PostgreSQL** | 16 | Main database |
| **SQLAlchemy** | 2.0.30 | Async ORM |
| **Alembic** | 1.13.1 | Database migrations |
| **Redis** | 7 | Caching + Message broker |
| **Celery** | 5.3.6 | Background task queue |
| **Flower** | 2.0.1 | Task monitoring |
| **JWT** | — | Authentication |
| **SlowAPI** | 0.1.9 | Rate limiting |
| **Resend** | 2.2.0 | Email notifications |
| **Pytest** | 8.2.0 | Testing |
| **Docker** | — | Containerization |
| **GitHub Actions** | — | CI/CD |
| **Render** | — | Cloud deployment |

---

## 📁 Project Structure

```
Booking-System/
├── main.py
├── requirements.txt
├── pytest.ini
├── alembic.ini
├── render.yaml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── limiter.py
│   │   └── celery_app.py
│   ├── models/
│   │   ├── user.py
│   │   ├── booking.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── booking.py
│   │   └── task.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── bookings.py
│   │   └── tasks.py
│   ├── tasks/
│   │   └── email_tasks.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── booking_service.py
│   │   ├── task_service.py
│   │   ├── cache_service.py
│   │   └── email_service.py
│   └── dependencies.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_bookings.py
│   └── test_tasks.py
└── .github/
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

---

## Why Booking Tasks?

Tasks in this system are **not generic todos** — they are travel workflow items that track a user's booking journey end-to-end:

| Task Example | Category | Status Flow |
|-------------|----------|-------------|
| "Book Flight to Paris" | travel | pending → booked |
| "Arrange Airport Transfer" | travel | pending → booked |
| "Prepare Business Docs" | business | pending → booked |
| "Hotel Check-in Reminder" | leisure | pending → booked |

Tasks allow users to plan and track everything related to their trip — from pre-booking research to post-booking actions — all in one place.

---

## Local Setup (Without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/princekushwaha9142/Booking-System.git
cd Booking-System

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your DATABASE_URL, REDIS_URL and RESEND_API_KEY

# 5. Create the database
psql -U postgres -c "CREATE DATABASE booking_db;"

# 6. Run migrations
alembic upgrade head

# 7. Start all services (3 terminals)

# Terminal 1 — API server
uvicorn main:app --reload

# Terminal 2 — Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Terminal 3 — Flower monitor (optional)
celery -A app.core.celery_app flower --port=5555
```

Visit **http://127.0.0.1:8000/docs** for Swagger UI.  
Visit **http://127.0.0.1:5555** for Flower task monitor.

---

## 🐳 Docker Setup

```bash
cp .env.example .env
docker compose up --build
```

One command starts API + PostgreSQL + Redis together! 

```bash
# Run in background
docker compose up -d

# Stop all containers
docker compose down
```

---

## Database Migrations (Alembic)

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "your message"

# Apply all migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View migration history
alembic history
```

---

## Testing

```bash
# Create test database
psql -U postgres -c "CREATE DATABASE booking_test;"

# Run all tests
pytest tests/ -v
```

**Result: 12/12 Passed ✅**

| Test File | Tests | Status |
|-----------|-------|--------|
| `test_auth.py` | 5 | ✅ Passed |
| `test_bookings.py` | 4 | ✅ Passed |
| `test_tasks.py` | 3 | ✅ Passed |
| **Total** | **12** | **✅ 12/12** |

---

## ⚡ Performance Metrics

| Metric | Value |
|--------|-------|
| Search response (uncached) | ~445ms |
| Search response (cached) | ~335ms |
| Cache improvement | ~25% faster |
| Test coverage | 12/12 (100%) |
| Auth rate limit | 5–10 req/min |
| Search rate limit | 30 req/min |
| Booking rate limit | 20 req/min |

---

## Authentication Flow

```
POST /api/v1/auth/register   → Create account        [5 req/min]
POST /api/v1/auth/login      → Get JWT tokens         [10 req/min]
POST /api/v1/auth/refresh    → Refresh access token   [10 req/min]
GET  /api/v1/auth/me         → Get current user
```

All protected routes require:
```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### Bookings

| Method | Endpoint | Auth | Rate Limit |
|--------|----------|------|------------|
| POST | `/api/v1/bookings/search/hotels` | ❌ | 30/min |
| POST | `/api/v1/bookings/search/flights` | ❌ | 30/min |
| POST | `/api/v1/bookings/hotels` | ✅ | 20/min |
| POST | `/api/v1/bookings/flights` | ✅ | 20/min |
| GET | `/api/v1/bookings/` | ✅ | — |
| GET | `/api/v1/bookings/{id}` | ✅ | — |
| PATCH | `/api/v1/bookings/{id}` | ✅ | — |
| DELETE | `/api/v1/bookings/{id}` | ✅ | — |

### ✅ Booking Tasks

| Method | Endpoint | Auth | Rate Limit |
|--------|----------|------|------------|
| POST | `/api/v1/tasks/` | ✅ | 30/min |
| GET | `/api/v1/tasks/` | ✅ | — |
| GET | `/api/v1/tasks/{id}` | ✅ | — |
| PATCH | `/api/v1/tasks/{id}` | ✅ | — |
| DELETE | `/api/v1/tasks/{id}` | ✅ | — |

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| Register | 5 req/min |
| Login | 10 req/min |
| Token Refresh | 10 req/min |
| Search Hotels/Flights | 30 req/min |
| Create Booking | 20 req/min |
| Create Task | 30 req/min |

---

## 📧 Email Notifications (Celery + Resend)

Real emails sent via **Resend** through **Celery task queue**:

- ✅ Booking confirmed → confirmation email
- ❌ Booking cancelled → cancellation email
- 📝 New task created → task notification email

**How it works:**
```
FastAPI → Redis Queue (DB 1) → Celery Worker → Resend API → Email
```

- Auto-retry on failure (3 retries, 60s delay)
- Tasks persist even if server crashes
- Monitor tasks via Flower dashboard at `http://localhost:5555`

Set `RESEND_API_KEY` in environment variables to enable.

---

## ☁️ Deploy to Render

1. Push code to GitHub (with `render.yaml`)
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your GitHub repository
4. Render auto-reads `render.yaml` and sets up API + PostgreSQL
5. Add `RENDER_DEPLOY_HOOK_URL` to GitHub Secrets for auto-deploy

Auto-deploy triggers on every push to `main` branch via GitHub Actions. 🚀

---

## Key Design Decisions

**Redis — 3 Databases:**
- `DB 0` → API caching (search results, bookings lists)
- `DB 1` → Celery broker (task queue)
- `DB 2` → Celery results (task status)

**Redis Caching Strategy**
- Search results cached for 5–10 minutes
- User booking/task lists cached with composite keys
- Cache auto-invalidated on every write operation

**JWT Strategy**
- Short-lived access tokens (30 min)
- Long-lived refresh tokens (7 days)
- Token type embedded in payload to prevent misuse

**Async Architecture**
- Fully async: router → service → database
- Uses `asyncpg` + SQLAlchemy async
- Redis via `redis.asyncio` — no thread blocking

**Celery + Redis (Message Broker)**
- Background tasks offloaded to Celery workers
- Redis as broker — same instance, different DB
- Retry logic built-in — tasks never lost on crash

---

## ⚙️ Environment Variables

```env
APP_NAME=Booking System
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/booking_db

REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

RESEND_API_KEY=re_xxxxxxxxxxxx
FROM_EMAIL=onboarding@resend.dev
```

---

## 👨‍💻 Author

**Prince Kushwaha**  
GitHub: [@princekushwaha9142](https://github.com/princekushwaha9142)

---

## 📄 License

MIT License — feel free to use and modify.