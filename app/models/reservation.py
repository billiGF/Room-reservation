from core.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))