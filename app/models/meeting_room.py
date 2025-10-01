from sqlalchemy import Column, String, Text, Integer
from core.db import Base


class MeetingRoom(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
