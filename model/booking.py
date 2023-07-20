from datetime import datetime
from pydantic import BaseModel, Field, validator


class Booking(BaseModel):
    id: str = ''
    table_id: str
    user_id: str
    booking_start_time: datetime = Field(include=True)

    @validator("booking_start_time")
    def ensure_date_range(cls, v):
        if not 12 <= v.hour <= 20:
            raise ValueError("Must be between 12:00 and 22:00")
        if datetime.now() >= v.replace(tzinfo=None):
            raise ValueError("This date has passed")
        return v