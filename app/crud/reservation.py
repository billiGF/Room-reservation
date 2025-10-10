from .base import CRUDbase
from models.reservation import Reservation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CRUDReservation(CRUDbase):
    async def get_reservations_at_the_same_time(
            self,
            from_reserve,
            to_reserve,
            meetingroom_id,
            session: AsyncSession):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
                )
            )
        reservations = reservations.scalars().all()
        return reservations 
    

reservation_crud = CRUDReservation(Reservation)