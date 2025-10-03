from fastapi import APIRouter, HTTPException, Depends
from crud.meeting_room import create_meeting_room, get_room_id_by_name, get_all_meetingroom, get_meeting_room_by_id, update_meeting_room
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
    room_id = await get_room_id_by_name(meeting_room.name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )
    new_room = await create_meeting_room(meeting_room, session)
    return new_room 

@router.get('/meeting_rooms/')
async def get_all_meetingrooms(session: AsyncSession = Depends(get_async_session)):
    all_meetingrooms = await get_all_meetingroom(session)
    return all_meetingrooms


@router.get('/magazine/{id}')
async def updatint_meeting_rooms(room_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await get_meeting_room_by_id(room_id,  session)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail='Not found'
        )
    return result

@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Получаем объект из БД по ID.
    # В ответ ожидается либо None, либо объект класса MeetingRoom.
    meeting_room = await get_meeting_room_by_id(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            # Для отсутствующего объекта вернем статус 404 — Not found.
            status_code=404, 
            detail='Переговорка не найдена!'
        )
    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)
    # Передаём в корутину все необходимые для обновления данные.
    meeting_room = await update_meeting_room(
        meeting_room, obj_in, session
    )
    return meeting_room
    

async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        ) 
