from pydantic import BaseModel, root_validator, validator
from datetime import datetime


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime
    

# Схема для полученных данных.
class ReservationUpdate(ReservationBase):
    pass


# Схема для полученных данных.
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



# Схема для возвращаемого объекта.
class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        orm_mode = True 