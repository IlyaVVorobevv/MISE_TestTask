from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, time

from app.models.booking import Booking


class BookingRepository:
    # Использую репозиторий для связи с бд, чтобы разделить обязанности между слоями

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, booking_id: int) -> Booking | None:  # Получаем бронь по id
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, booking: Booking) -> Booking:   # Создание брони
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def get_all(self, booking_date: date | None = None) -> list[Booking]:
        query = select(Booking).order_by(Booking.booking_date,Booking.booking_time)

        if booking_date is not None:
            query = query.where(Booking.booking_date == booking_date)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_active_booking_by_slot(self, booking_date: date, booking_time: time) -> Booking | None:
        query = select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == "active",
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def cancel_booking(self, booking: Booking) -> Booking:
        booking.status = "cancelled"
        await self.db.commit()
        await self.db.refresh(booking)
        return booking
