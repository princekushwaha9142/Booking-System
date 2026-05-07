from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING   = "pending"
    BOOKED    = "booked"
    CANCELLED = "cancelled"


class TaskCategory(str, enum.Enum):
    TRAVEL   = "travel"
    BUSINESS = "business"
    LEISURE  = "leisure"
    OTHER    = "other"


class BookingTask(Base):
    __tablename__ = "booking_tasks"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title       = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(Enum(TaskStatus),   default=TaskStatus.PENDING,     nullable=False)
    category    = Column(Enum(TaskCategory), default=TaskCategory.OTHER,     nullable=True)
    due_date    = Column(DateTime(timezone=True), nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="tasks")