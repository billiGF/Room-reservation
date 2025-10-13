from pydantic import BaseModel, root_validator, validator, Extra, Field
from datetime import datetime, timedelta
from typing import Optional

FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(examples=[FROM_TIME])
    to_reserve: datetime = Field(examples=[TO_TIME])

    class Config:
        extra = Extra.forbid
    

class ReservationUpdate(ReservationBase):
    pass


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int

    @validator('from_reserve')

    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['to_reserve'] <= values['from_reserve']:
            raise ValueError('Error reserving')
        return values    



class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        fron_attributes = True 