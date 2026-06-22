# ✈️ Booking System API

![CI](https://github.com/princekushwaha9142/Booking-System/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/princekushwaha9142/Booking-System/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Alembic](https://img.shields.io/badge/Alembic-1.13.1-blue)
![Pytest](https://img.shields.io/badge/Tests-12%2F12%20Passed-brightgreen?logo=pytest)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?logo=jsonwebtokens)
![License](https://img.shields.io/badge/License-MIT-green)

A production-ready REST API for hotel and flight bookings built with FastAPI, PostgreSQL, Redis, and JWT Authentication.

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.111.0 | Web framework |
| **PostgreSQL** | 16 | Main database |
| **SQLAlchemy** | 2.0.30 | Async ORM |
| **Alembic** | 1.13.1 | Database migrations |
| **Redis** | 7 | Caching |
| **JWT** | — | Authentication |
| **SlowAPI** | 0.1.9 | Rate limiting |
| **BackgroundTasks** | — | Email notifications |
| **Pytest** | 8.2.0 | Testing |
| **Docker** | — | Containerization |
| **GitHub Actions** | — | CI/CD |
| **Render** | — | Cloud deployment |

---

## 📁 Project Structure

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

│   │   ├── config.py        # App settings from .env

│   │   ├── database.py      # Async SQLAlchemy engine

│   │   ├── security.py      # JWT + bcrypt

│   │   └── limiter.py       # SlowAPI rate limiter

│   ├── models/

│   │   ├── user.py          # User table

│   │   ├── booking.py       # Bookings table

│   │   └── task.py          # Tasks table

│   ├── schemas/

│   │   ├── user.py          # User Pydantic schemas

│   │   ├── booking.py       # Booking schemas

│   │   └── task.py          # Task schemas

│   ├── routers/

│   │   ├── auth.py          # Auth routes

│   │   ├── bookings.py      # Booking routes

│   │   └── tasks.py         # Task routes

│   ├── services/

│   │   ├── auth_service.py     # Auth business logic

│   │   ├── booking_service.py  # Booking logic + Redis cache

│   │   ├── task_service.py     # Task CRUD logic

│   │   ├── cache_service.py    # Redis operations

│   │   └── email_service.py    # Background email notifications

│   └── dependencies.py         # JWT guard (get_current_user)

├── tests/

│   ├── conftest.py          # Fixtures + test DB setup

│   ├── test_auth.py         # Auth tests

│   ├── test_bookings.py     # Booking tests

│   └── test_tasks.py        # Task tests

└── .github/

└── workflows/

├── ci.yml           # Run tests on every push

└── deploy.yml       # Auto deploy to Render on main
---

## 🚀 Local Setup (Without Docker)

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
# Edit .env with your DATABASE_URL and REDIS_URL

# 5. Create the database
psql -U postgres -c "CREATE DATABASE booking_db;"

# 6. Run migrations
alembic upgrade head

# 7. Start the server
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for Swagger UI.

---

## 🐳 Docker Setup

```bash
cp .env.example .env
docker compose up --build
```

One command starts API + PostgreSQL + Redis together! ✅

```bash
# Run in background
docker compose up -d

# Stop all containers
docker compose down
```

---

## 🗄️ Database Migrations (Alembic)

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

## 🧪 Testing

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

## 🔑 Authentication Flow

POST /api/v1/auth/register   → Create account        [5 req/min]

POST /api/v1/auth/login      → Get JWT tokens         [10 req/min]

POST /api/v1/auth/refresh    → Refresh access token   [10 req/min]

GET  /api/v1/auth/me         → Get current user

All protected routes require:
Authorization: Bearer <access_token>

---

## 📋 API Endpoints

### 🏨 Bookings

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

### ✅ Tasks

| Method | Endpoint | Auth | Rate Limit |
|--------|----------|------|------------|
| POST | `/api/v1/tasks/` | ✅ | 30/min |
| GET | `/api/v1/tasks/` | ✅ | — |
| GET | `/api/v1/tasks/{id}` | ✅ | — |
| PATCH | `/api/v1/tasks/{id}` | ✅ | — |
| DELETE | `/api/v1/tasks/{id}` | ✅ | — |

---

## ⚙️ Environment Variables

```env
APP_NAME=BookingSystem
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your-secret-key-here

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/booking_db
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
```

---

## 🔒 Rate Limiting

| Endpoint | Limit |
|----------|-------|
| Register | 5 req/min |
| Login | 10 req/min |
| Token Refresh | 10 req/min |
| Search Hotels/Flights | 30 req/min |
| Create Booking | 20 req/min |
| Create Task | 30 req/min |

---

## 📧 Background Email Notifications

Email notifications are sent automatically in the background for:
- ✅ Booking confirmed
- ❌ Booking cancelled
- 📝 New task created

> Currently logs to console. Replace with SMTP/SendGrid in production.

---

## ☁️ Deploy to Render

1. Push code to GitHub (with `render.yaml`)
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your GitHub repository
4. Render auto-reads `render.yaml` and sets up API + PostgreSQL
5. Add `RENDER_DEPLOY_HOOK_URL` to GitHub Secrets for auto-deploy

Auto-deploy triggers on every push to `main` branch via GitHub Actions. 🚀

---

## 🧠 Key Design Decisions

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

---

## 👨‍💻 Author

**Prince Kushwaha**

GitHub: [@princekushwaha9142](https://github.com/princekushwaha9142)

---

## 📄 License

MIT License — feel free to use and modify.