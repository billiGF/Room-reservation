from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.meeting_room import meeting_room_crud
from crud.reservation import reservation_crud

from models.meeting_room import MeetingRoom # Not uset yet

async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )

        
async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
):
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room 


async def check_reservation_intersections(**kwargs):
    info = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if info is not None:
        raise HTTPException(
            status_code=422,
            detail={info}
        )
    

async def check_reservation_before_edit(
        reservation_id: int, 
        session: AsyncSession):
    info = await reservation_crud.remove(reservation_id, session)
    if info is None:
        raise HTTPException(
            status_code=404,
            detail=f'Reservation {reservation_id}, not found!'
        )
    return info