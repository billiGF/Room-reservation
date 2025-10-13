from fastapi import APIRouter, Depends
from schema.reservation import ReservationCreate, ReservationDB, ReservationUpdate
from core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.validators import check_reservation_intersections, check_meeting_room_exists, check_reservation_before_edit
from crud.reservation import reservation_crud

from core.user import current_user, current_superuser
from models import User


router = APIRouter()




@router.post('/', response_model=ReservationDB)
async def create_reservation(
        reservation: ReservationCreate, 
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
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
        session,
        user
        )
    return result



@router.get(
        '/',
        dependencies=[Depends(current_superuser)])
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
    ):
    info = await reservation_crud.get_multi(session)
    return info



@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для суперюзеров или создателей объекта бронирования."""
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    delete = await reservation_crud.remove(
        reservation, 
        session
        )
    return {"Reservation": f"{reservation_id} Deleted"}



@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для суперюзеров или создателей объекта бронирования."""
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
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


@router.get(
    '/my_reservation',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
    )
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    info = await reservation_crud.get_by_user(session, user)
    return info