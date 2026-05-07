import uuid
import hashlib
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.booking import Booking, BookingType, BookingStatus
from app.schemas.booking import (
    HotelBookingCreate, FlightBookingCreate,
    BookingUpdate, HotelSearchParams, FlightSearchParams,
)
from app.services.cache_service import cache_service


def _make_reference() -> str:
    return uuid.uuid4().hex[:12].upper()


async def search_hotels(params: HotelSearchParams) -> list[dict]:
    key = cache_service.search_key(
        "hotel",
        hashlib.md5(params.model_dump_json().encode()).hexdigest(),
    )
    cached = await cache_service.get(key)
    if cached:
        return cached

    # Swap this block for a real hotel provider API call
    results = [
        {
            "hotel_name":     f"Grand {params.location} Hotel",
            "location":       params.location,
            "room_type":      params.room_type or "Standard",
            "price_per_night": 120.0,
            "available":      True,
        },
        {
            "hotel_name":     f"{params.location} Boutique Inn",
            "location":       params.location,
            "room_type":      params.room_type or "Deluxe",
            "price_per_night": 85.0,
            "available":      True,
        },
    ]
    await cache_service.set(key, results, ttl=600)
    return results


async def search_flights(params: FlightSearchParams) -> list[dict]:
    key = cache_service.search_key(
        "flight",
        hashlib.md5(params.model_dump_json().encode()).hexdigest(),
    )
    cached = await cache_service.get(key)
    if cached:
        return cached

    results = [
        {
            "airline":         "SkyWings",
            "flight_number":   "SW101",
            "origin":          params.origin,
            "destination":     params.destination,
            "departure":       str(params.departure_date),
            "seat_class":      params.seat_class,
            "price":           350.0,
            "available_seats": 42,
        },
        {
            "airline":         "AirExpress",
            "flight_number":   "AE202",
            "origin":          params.origin,
            "destination":     params.destination,
            "departure":       str(params.departure_date),
            "seat_class":      params.seat_class,
            "price":           290.0,
            "available_seats": 15,
        },
    ]
    await cache_service.set(key, results, ttl=300)
    return results


async def create_hotel_booking(
    db: AsyncSession, user_id: int, data: HotelBookingCreate
) -> Booking:
    booking = Booking(
        user_id=user_id,
        booking_type=BookingType.HOTEL,
        reference_number=_make_reference(),
        title=f"Hotel: {data.hotel_name}",
        description=data.description,
        total_price=data.total_price,
        currency=data.currency,
        check_in_date=data.check_in_date,
        check_out_date=data.check_out_date,
        hotel_name=data.hotel_name,
        hotel_location=data.hotel_location,
        room_type=data.room_type,
        num_guests=data.num_guests,
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    await cache_service.delete_pattern(f"user:{user_id}:bookings:*")
    return booking


async def create_flight_booking(
    db: AsyncSession, user_id: int, data: FlightBookingCreate
) -> Booking:
    booking = Booking(
        user_id=user_id,
        booking_type=BookingType.FLIGHT,
        reference_number=_make_reference(),
        title=f"Flight: {data.origin} → {data.destination}",
        description=data.description,
        total_price=data.total_price,
        currency=data.currency,
        check_in_date=data.check_in_date,
        check_out_date=data.check_out_date,
        airline=data.airline,
        flight_number=data.flight_number,
        origin=data.origin,
        destination=data.destination,
        seat_class=data.seat_class,
        num_passengers=data.num_passengers,
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    await cache_service.delete_pattern(f"user:{user_id}:bookings:*")
    return booking


async def get_user_bookings(
    db: AsyncSession,
    user_id: int,
    booking_type: Optional[str] = None,
    booking_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> dict:
    suffix = f"{booking_type}:{booking_status}:{skip}:{limit}"
    cache_key = cache_service.user_bookings_key(user_id, suffix)
    cached = await cache_service.get(cache_key)
    if cached:
        return cached

    query = select(Booking).where(Booking.user_id == user_id)
    if booking_type:
        query = query.where(Booking.booking_type == booking_type)
    if booking_status:
        query = query.where(Booking.status == booking_status)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    rows  = (await db.execute(query.offset(skip).limit(limit).order_by(Booking.created_at.desc()))).scalars().all()

    data = {
        "total": total,
        "bookings": [
            {k: str(v) if not isinstance(v, (int, float, bool, type(None), str)) else v
             for k, v in b.__dict__.items() if not k.startswith("_")}
            for b in rows
        ],
    }
    await cache_service.set(cache_key, data)
    return data


async def get_booking_by_id(db: AsyncSession, booking_id: int, user_id: int) -> Booking:
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id)
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


async def update_booking(
    db: AsyncSession, booking_id: int, user_id: int, data: BookingUpdate
) -> Booking:
    booking = await get_booking_by_id(db, booking_id, user_id)
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update a cancelled booking")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(booking, field, value)

    await db.flush()
    await db.refresh(booking)
    await cache_service.delete(cache_service.booking_key(booking_id))
    await cache_service.delete_pattern(f"user:{user_id}:bookings:*")
    return booking


async def cancel_booking(db: AsyncSession, booking_id: int, user_id: int) -> Booking:
    booking = await get_booking_by_id(db, booking_id, user_id)
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already cancelled")

    booking.status = BookingStatus.CANCELLED
    await db.flush()
    await db.refresh(booking)
    await cache_service.delete(cache_service.booking_key(booking_id))
    await cache_service.delete_pattern(f"user:{user_id}:bookings:*")
    return booking