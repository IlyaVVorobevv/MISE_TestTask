from datetime import date, time, datetime

from app.db import Base
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    booking_date: Mapped[date] = mapped_column(nullable=False, index=True)
    booking_time: Mapped[time] = mapped_column(nullable=False)
    guests: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

