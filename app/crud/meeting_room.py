from typing import Optional
from sqlalchemy import select, update
# Импортируем sessionmaker из файла с настройками БД.


from models.meeting_room import MeetingRoom
from schema.meeting_room import MeetingRoomCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession
        ) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room 


async def get_room_id_by_name(
        room_name: str, 
        session: AsyncSession
        ) -> Optional[int]:
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
        MeetingRoom.name == room_name
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id 


async def get_all_meetingroom(
        session: AsyncSession
        ):
    info = await session.execute(
        select(MeetingRoom)
    )
    info = info.scalars().all()
    return info


async def get_meeting_room_by_id(
        room_id: int,
        session: AsyncSession
        ):
    db_room = await session.execute(
        select(MeetingRoom).where(
            MeetingRoom.id == room_id
        )
    )
    db_room = db_room.scalars().first()
    return db_room


async def update_meeting_room(
        db_room: MeetingRoom,
        room_id: MeetingRoomCreate, 
        session: AsyncSession
        ):
    obj_data = jsonable_encoder(db_room)
    update_data = room_id.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_room, key, value)    

    #Same result but differnet code One Is Middle Cod another is Junior
    for field in obj_data:
        if field in update_data:
            setattr(db_room, field, update_data[field])
    
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room