from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import create_tables
from app.core.limiter import limiter
from app.services.cache_service import cache_service
from app.routers import auth, bookings, tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    await create_tables()
    await cache_service.connect()
    yield
    await cache_service.disconnect()
    logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hotel & Flight Booking API with JWT + Redis",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(tasks.router,    prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse({"status": "ok", "version": settings.APP_VERSION})


@app.get("/", tags=["Health"])
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}