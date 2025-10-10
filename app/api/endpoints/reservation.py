from fastapi import APIRouter, Depends
from schema.reservation import ReservationCreate, ReservationDB, ReservationUpdate
from core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.validators import check_reservation_intersections, check_meeting_room_exists, check_reservation_before_edit
from crud.reservation import reservation_crud

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate, 
    session: AsyncSession = Depends(get_async_session)
    ):
    await check_meeting_room_exists(
        reservation.meetingroom_id, 
        session
        )
    await check_reservation_intersections(
        **reservation.dict(), 
        session=session
        )
    result = await reservation_crud.create(
        reservation, 
        session
        )
    return result



@router.get('/')
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
    ):
    info = await reservation_crud.get_multi(session)
    return info



@router.delete('/{reservation}')
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session)
    ):
    info = await check_reservation_before_edit(
        reservation_id, 
        session
        )
    delete = await reservation_crud.remove(
        info, 
        session
        )
    return {"Reservation": f"{reservation_id} Deleted"}



@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session 
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session,
    )
    return reservation 