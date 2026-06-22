from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.dependencies import get_current_user
from app.models.user import User
from app.models.booking import BookingType, BookingStatus
from app.schemas.booking import (
    HotelBookingCreate, FlightBookingCreate, BookingUpdate,
    BookingResponse, BookingListResponse,
    HotelSearchParams, FlightSearchParams,
)
from app.services import booking_service
from app.services.email_service import notify_booking_confirmed, notify_booking_cancelled

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/search/hotels")
@limiter.limit("30/minute")
async def search_hotels(request: Request, params: HotelSearchParams):
    return await booking_service.search_hotels(params)


@router.post("/search/flights")
@limiter.limit("30/minute")
async def search_flights(request: Request, params: FlightSearchParams):
    return await booking_service.search_flights(params)


@router.post("/hotels", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def book_hotel(
    request: Request,
    data: HotelBookingCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = await booking_service.create_hotel_booking(db, current_user.id, data)
    notify_booking_confirmed(
        background_tasks,
        email=current_user.email,
        name=current_user.full_name or current_user.username,
        reference=booking.reference_number,
        title=booking.title,
    )
    return booking


@router.post("/flights", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def book_flight(
    request: Request,
    data: FlightBookingCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = await booking_service.create_flight_booking(db, current_user.id, data)
    notify_booking_confirmed(
        background_tasks,
        email=current_user.email,
        name=current_user.full_name or current_user.username,
        reference=booking.reference_number,
        title=booking.title,
    )
    return booking


@router.get("/", response_model=BookingListResponse)
async def list_bookings(
    booking_type:   Optional[BookingType]   = Query(None),
    booking_status: Optional[BookingStatus] = Query(None),
    skip:  int = Query(0,  ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await booking_service.get_user_bookings(
        db, current_user.id,
        booking_type=booking_type.value   if booking_type   else None,
        booking_status=booking_status.value if booking_status else None,
        skip=skip, limit=limit,
    )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await booking_service.get_booking_by_id(db, booking_id, current_user.id)


@router.patch("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await booking_service.update_booking(db, booking_id, current_user.id, data)


@router.delete("/{booking_id}", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = await booking_service.cancel_booking(db, booking_id, current_user.id)
    notify_booking_cancelled(
        background_tasks,
        email=current_user.email,
        name=current_user.full_name or current_user.username,
        reference=booking.reference_number,
        title=booking.title,
    )
    return booking