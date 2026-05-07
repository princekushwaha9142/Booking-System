from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models.booking import BookingType, BookingStatus


class HotelSearchParams(BaseModel):
    location:   str
    check_in:   datetime
    check_out:  datetime
    num_guests: int = 1
    room_type:  Optional[str]   = None
    max_price:  Optional[float] = None


class FlightSearchParams(BaseModel):
    origin:          str
    destination:     str
    departure_date:  datetime
    return_date:     Optional[datetime] = None
    num_passengers:  int = 1
    seat_class:      Optional[str] = "economy"


class HotelBookingCreate(BaseModel):
    hotel_name:     str
    hotel_location: str
    room_type:      str
    check_in_date:  datetime
    check_out_date: datetime
    num_guests:     int = 1
    total_price:    float
    currency:       str = "USD"
    description:    Optional[str] = None

    @field_validator("check_out_date")
    @classmethod
    def checkout_after_checkin(cls, v, info):
        if info.data.get("check_in_date") and v <= info.data["check_in_date"]:
            raise ValueError("Check-out must be after check-in")
        return v


class FlightBookingCreate(BaseModel):
    airline:        str
    flight_number:  str
    origin:         str
    destination:    str
    check_in_date:  datetime    # departure
    check_out_date: datetime    # arrival
    seat_class:     str = "economy"
    num_passengers: int = 1
    total_price:    float
    currency:       str = "USD"
    description:    Optional[str] = None


class BookingUpdate(BaseModel):
    status:      Optional[BookingStatus] = None
    description: Optional[str]          = None
    total_price: Optional[float]        = None


class BookingResponse(BaseModel):
    id:               int
    user_id:          int
    booking_type:     BookingType
    status:           BookingStatus
    reference_number: str
    title:            str
    description:      Optional[str]
    total_price:      float
    currency:         str
    check_in_date:    datetime
    check_out_date:   datetime
    hotel_name:       Optional[str]
    hotel_location:   Optional[str]
    room_type:        Optional[str]
    num_guests:       Optional[int]
    airline:          Optional[str]
    flight_number:    Optional[str]
    origin:           Optional[str]
    destination:      Optional[str]
    seat_class:       Optional[str]
    num_passengers:   Optional[int]
    created_at:       datetime

    model_config = {"from_attributes": True}


class BookingListResponse(BaseModel):
    total:    int
    bookings: list[BookingResponse]