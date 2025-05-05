from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v: datetime, values) -> datetime:
        if 'start_time' in values.data and v <= values.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)