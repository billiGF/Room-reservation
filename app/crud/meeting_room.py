from sqlalchemy import select

from crud.base import CRUDbase
from sqlalchemy.ext.asyncio import AsyncSession

from models.meeting_room import MeetingRoom


class CRUDMeetingroom(CRUDbase):

    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession):
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id
    
meeting_room_crud = CRUDMeetingroom(MeetingRoom)