from sqlalchemy import Column, String, Text, Integer
from core.database import Base


class MeetingRoom(Base):
    name = Column(String(100), unique=True, nullable=False)
    decsription = Column(Text)
    age = Column(Integer)