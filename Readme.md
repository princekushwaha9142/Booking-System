# ✈️ Booking System API

A production-ready REST API for hotel and flight bookings built with **FastAPI**, **PostgreSQL**, **Redis**, and **JWT Authentication**.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Main database |
| **SQLAlchemy (Async)** | ORM |
| **Redis** | Caching |
| **JWT** | Authentication |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |

---

## 📁 Project Structure

```
Booking-System/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── app/
    ├── core/
    │   ├── config.py        # App settings (reads .env)
    │   ├── database.py      # Async SQLAlchemy setup
    │   └── security.py      # JWT + bcrypt
    ├── models/
    │   ├── user.py          # User table
    │   ├── booking.py       # Bookings table
    │   └── task.py          # Tasks table
    ├── schemas/
    │   ├── user.py          # User request/response schemas
    │   ├── booking.py       # Booking schemas
    │   └── task.py          # Task schemas
    ├── routers/
    │   ├── auth.py          # Auth endpoints
    │   ├── bookings.py      # Booking endpoints
    │   └── tasks.py         # Task endpoints
    ├── services/
    │   ├── auth_service.py     # Auth logic
    │   ├── booking_service.py  # Booking logic
    │   ├── task_service.py     # Task logic
    │   └── cache_service.py    # Redis caching
    └── dependencies.py      # JWT guard (get_current_user)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/Booking-System.git
cd Booking-System

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your database and redis credentials

# 5. Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE booking_db;"

# 6. Run the server
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for Swagger UI.

---

## 🔑 Authentication Flow

```
POST /api/v1/auth/register   → Create account
POST /api/v1/auth/login      → Get access + refresh token
POST /api/v1/auth/refresh    → Refresh expired token
GET  /api/v1/auth/me         → Get current user
```

All protected routes require:
```
Authorization: Bearer <access_token>
```

---

## 📋 API Endpoints

### 🏨 Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/bookings/search/hotels` | Search hotels |
| POST | `/api/v1/bookings/search/flights` | Search flights |
| POST | `/api/v1/bookings/hotels` | Book a hotel 🔒 |
| POST | `/api/v1/bookings/flights` | Book a flight 🔒 |
| GET | `/api/v1/bookings/` | List all bookings 🔒 |
| GET | `/api/v1/bookings/{id}` | Get booking by ID 🔒 |
| PATCH | `/api/v1/bookings/{id}` | Update booking 🔒 |
| DELETE | `/api/v1/bookings/{id}` | Cancel booking 🔒 |

### ✅ Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks/` | Create task 🔒 |
| GET | `/api/v1/tasks/` | List all tasks 🔒 |
| GET | `/api/v1/tasks/{id}` | Get task by ID 🔒 |
| PATCH | `/api/v1/tasks/{id}` | Update task 🔒 |
| DELETE | `/api/v1/tasks/{id}` | Delete task 🔒 |

🔒 = Requires JWT token

---

## ⚙️ Environment Variables

```env
APP_NAME=BookingSystem
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/booking_db
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
```

---

## 🧪 Example Requests

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user123","password":"12345678"}'
```

### Book a Hotel
```bash
curl -X POST http://127.0.0.1:8000/api/v1/bookings/hotels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_name": "Grand Mumbai Hotel",
    "hotel_location": "Mumbai, India",
    "room_type": "Deluxe",
    "check_in_date": "2026-06-01T14:00:00",
    "check_out_date": "2026-06-05T11:00:00",
    "num_guests": 2,
    "total_price": 480.00
  }'
```

### Create a Task
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tasks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Book Flight to Delhi",
    "description": "Economy class preferred",
    "category": "travel"
  }'
```

---

## 👨‍💻 Author

**Prince** 