from fastapi import HTTPException, status
from datetime import date, time

from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate
from app.models.booking import Booking


class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository


    async def create_booking(self, create_booking: BookingCreate) -> Booking:

        new_booking = Booking(
            name=create_booking.name,
            phone=create_booking.phone,
            booking_date=create_booking.booking_date,
            booking_time=create_booking.booking_time,
            guests=create_booking.guests
        )

        return await self.booking_repository.create(new_booking)

    async def list_bookings(self, booking_date: date | None = None) -> list[Booking]:
        return await self.booking_repository.get_all(booking_date)

    async def get_booking(self, booking_id: int) -> Booking:
        return await self.booking_repository.get_booking(booking_id)

    async def cancel_booking(self, booking_id: int) -> Booking:
        return await self.booking_repository.cancel_booking(booking_id)

    async def _ensure_slot_is_free(self, booking_date: date, booking_time: time) -> None:
        result = await self.booking_repository.ensure_slot_is_free(booking_date, booking_time)