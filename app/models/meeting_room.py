from sqlalchemy import Column, String, Text, Integer
from core.db import Base
from sqlalchemy.orm import relationship

class MeetingRoom(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    reservations = relationship('Reservation', cascade='delete')
