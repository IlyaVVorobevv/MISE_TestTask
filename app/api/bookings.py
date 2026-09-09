from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.schemas.booking import BookingCreate, BookingOut
from app.repositories.booking_repository import BookingRepository
from app.services.booking_service import BookingService
from app.db import get_db


async def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    repository = BookingRepository(db)
    return BookingService(repository)

router_booking = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)

@router_booking.post("",
                     response_model=BookingOut,
                     status_code=status.HTTP_201_CREATED,
                     summary="Создать бронь")
async def create_booking(booking_data: BookingCreate,
                         booking_service: BookingService = Depends(get_booking_service)
                         ) -> BookingOut:
    booking = await booking_service.create_booking(booking_data)
    return BookingOut.model_validate(booking)


@router_booking.get("",
                    response_model=list[BookingOut],
                    summary="Список броней")
async def get_all_bookings(date_booking: date | None = Query(
                                default=None, description="Фильтр по дате брони"
                           ),
                           booking_service: BookingService = Depends(get_booking_service)
                           ) -> list[BookingOut]:

    bookings = await booking_service.list_bookings(booking_date=date_booking)
    return [BookingOut.model_validate(booking) for booking in bookings]

@router_booking.get(
        "/{booking_id}",
        response_model=BookingOut,
        summary="Получить бронь по id",
        responses={404: {"description": "Бронь не найдена"}})
async def get_booking(booking_id: int,
                      service: BookingService = Depends(get_booking_service),
                     ) -> BookingOut:

        booking = await service.get_booking(booking_id)
        return BookingOut.model_validate(booking)


@router_booking.delete(
        "/{booking_id}",
        response_model=BookingOut,
        summary="Отменить бронь",
        responses={404: {"description": "Бронь не найдена"}})
async def cancel_booking(booking_id: int,
                         service: BookingService = Depends(get_booking_service)
                        ) -> BookingOut:

        booking = await service.cancel_booking(booking_id)

        return BookingOut.model_validate(booking)









