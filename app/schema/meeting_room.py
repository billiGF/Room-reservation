from typing import Optional
from pydantic import BaseModel, Field


# class MeetingRoomCreate(BaseModel):
#     name: str = Field(max_length=100)
#     description: Optional[str] = None

    # class Config:
    #     exclude_none = True #We dont need it at much
        
class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomCreate):
    id: int 

    class Config:
        from_attributes=True