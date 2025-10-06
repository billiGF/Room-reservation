from fastapi import APIRouter, HTTPException, Depends
# from crud.meeting_room import create_meeting_room, get_room_id_by_name, get_all_meetingroom, get_meeting_room_by_id, update_meeting_room
from crud.meeting_room import meeting_room_crud
from schema.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
from core.db import get_async_session, AsyncSession

router = APIRouter()


@router.post(
    '/meeting_rooms/', 
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
):
    room_id = await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room 


@router.get(
    '/meeting_all_rooms/'
    )
async def get_all_meetingrooms(
    session: AsyncSession = Depends(get_async_session)
    ):

    all_meetingrooms = await meeting_room_crud.get_multi(session)
    return all_meetingrooms


@router.get(
    '/magazine/{id}'
    )
async def updatint_meeting_rooms(
    room_id: int,
    session: AsyncSession = Depends(get_async_session)
    ):
    result = await meeting_room_crud.get(room_id,  session)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail='Not found'
        )
    return result


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await meeting_room_crud.update(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404, 
            detail='Переговорка не найдена!'
        )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room
    

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
    

# from sqlalchemy import select
# from models.meeting_room import MeetingRoom
# @router.get('/test/')
# async def test_table(id_s: int, session: AsyncSession = Depends(get_async_session),):
#     wait = await session.execute(select(MeetingRoom).where(MeetingRoom.id == id_s))
#     row = wait.scalars().first()
#     return row

from models.meeting_room import MeetingRoom
from sqlalchemy import delete
@router.delete('/{/meeting_room_id}')
async def delete_meeting_room(
    room_id: int,
    session: AsyncSession = Depends(get_async_session)
    ): 
    cheking_existing_room = await meeting_room_crud.get(room_id, session)
    if cheking_existing_room is None:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )
    id_meeting_room = cheking_existing_room.id 
    await session.delete(cheking_existing_room)
    await session.commit()
    return {f"Meetingroom {id_meeting_room}": "Deleted"}