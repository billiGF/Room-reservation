from typing import Optional
from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class MeetingRoomUpdate(MeetingRoomBase):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    

class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(min_length=4, max_length=100)


class MeetingRoomDB(MeetingRoomCreate):
    id: int 
    
    class Config:
        from_attributes=True