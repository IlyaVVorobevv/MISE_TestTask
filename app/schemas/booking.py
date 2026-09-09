from datetime import date, time
from pydantic import BaseModel, Field, ConfigDict, field_validator

import re


class BookingCreate(BaseModel):
    name: str = Field(min_length=2)
    phone: str = Field(examples=["+79991112233", "89991112233"])
    booking_date: date = Field(description="Дата бронирования", examples=["2026-09-10"])
    booking_time: time = Field(description="Время бронирования", examples=["18:00:00"])
    guests: int = Field(ge=1, le=12)

    @field_validator('phone')
    @classmethod
    def validate_ru_phone(cls, value: str) -> str:
        digits = re.sub(r'\D', '', value)
        if len(digits) == 11 and value[0] in ('7', '8'):
            return value
        raise ValueError(
            'Введите корректный номер: 7 или 8 и 10 цифр'
        )

class BookingOut(BaseModel):
    id: int
    status: str = Field(examples=["active", "cancelled"])

    model_config = ConfigDict(from_attributes=True)
