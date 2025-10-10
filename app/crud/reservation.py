from .base import CRUDbase
from models.reservation import Reservation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

class CRUDReservation(CRUDbase):
    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve,
            to_reserve,
            meetingroom_id,
            reservation_id: Optional[int] = None,
            session: AsyncSession)-> list[Reservation]:
        
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            from_reserve <= Reservation.to_reserve,
            to_reserve >= Reservation.from_reserve
            )    
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations 
    
    
    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
                select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations 


reservation_crud = CRUDReservation(Reservation)