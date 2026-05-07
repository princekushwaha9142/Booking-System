from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class BookingType(str, enum.Enum):
    HOTEL  = "hotel"
    FLIGHT = "flight"


class BookingStatus(str, enum.Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    booking_type     = Column(Enum(BookingType), nullable=False)
    status           = Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    reference_number = Column(String, unique=True, index=True, nullable=False)

    # Common
    title          = Column(String, nullable=False)
    description    = Column(Text, nullable=True)
    total_price    = Column(Float, nullable=False)
    currency       = Column(String, default="USD")
    check_in_date  = Column(DateTime(timezone=True), nullable=False)
    check_out_date = Column(DateTime(timezone=True), nullable=False)

    # Hotel-specific
    hotel_name     = Column(String, nullable=True)
    hotel_location = Column(String, nullable=True)
    room_type      = Column(String, nullable=True)
    num_guests     = Column(Integer, nullable=True)

    # Flight-specific
    airline        = Column(String, nullable=True)
    flight_number  = Column(String, nullable=True)
    origin         = Column(String, nullable=True)
    destination    = Column(String, nullable=True)
    seat_class     = Column(String, nullable=True)
    num_passengers = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="bookings")