from core.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    user_id = Column(Integer, ForeignKey('user.id',  name='fk_reservation_user_id_user'))

    def __repr__(self):
        return f"Reservated {self.from_reserve}, to {self.to_reserve}"

