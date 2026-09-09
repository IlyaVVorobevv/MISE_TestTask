from datetime import date, time

from fastapi import HTTPException, status

from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate
from app.models.booking import Booking


class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository


    async def create_booking(self, create_booking: BookingCreate) -> Booking:
        existing_booking = (
            await self.booking_repository.get_active_booking_by_slot(
                booking_date=create_booking.booking_date,
                booking_time=create_booking.booking_time,
            )
        )

        if existing_booking is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This time slot is already booked",
            )

        new_booking = Booking(
            name=create_booking.name,
            phone=create_booking.phone,
            booking_date=create_booking.booking_date,
            booking_time=create_booking.booking_time,
            guests=create_booking.guests,
            status="active"
        )

        return await self.booking_repository.create(new_booking)

    async def list_bookings(self, booking_date: date | None = None) -> list[Booking]:
        return await self.booking_repository.get_all(booking_date)

    async def get_booking(self, booking_id: int) -> Booking:
        booking = await self.booking_repository.get_by_id(booking_id)

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking

    async def cancel_booking(self, booking_id: int) -> Booking:
        booking = await self.booking_repository.get_by_id(booking_id)

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )

        if booking.status == "cancelled":
            return booking

        return await self.booking_repository.cancel_booking(booking)


