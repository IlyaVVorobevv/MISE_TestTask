from datetime import date, time, datetime, timedelta
import re

from pydantic import BaseModel, Field, ConfigDict, field_validator


class BookingCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=120,
        examples=["Иван Иванов"],
    )

    phone: str = Field(
        examples=["+79991112233", "89991112233"],
    )

    booking_date: date = Field(
        description="Дата бронирования",
        examples=["2026-09-10"],
    )

    booking_time: time = Field(
        description="Время бронирования",
        examples=["18:00"],
    )

    guests: int = Field(
        ge=1,
        le=12,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z\s-]+", value):
            raise ValueError(
                "Имя может содержать только буквы, пробелы и дефис"
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"(?:\+7|8)\d{10}", value):
            raise ValueError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
            )

        return value

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()

        if value < today:
            raise ValueError(
                "Дата бронирования не может быть раньше сегодняшней"
            )

        if value > today.replace(day=today.day) + timedelta(days=90):
            raise ValueError(
                "Дата бронирования не может быть более чем через 90 дней"
            )

        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError(
                "Бронирование возможно только на целый час"
            )

        if value.hour < 12 or value.hour > 22:
            raise ValueError(
                "Время бронирования должно быть с 12:00 до 22:00"
            )

        return value


class BookingOut(BookingCreate):
    id: int
    status: str = Field(
        examples=["active", "cancelled"],
    )
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )