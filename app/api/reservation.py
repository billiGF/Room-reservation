from fastapi import APIRouter, Depends
from crud.reservation import room_rervation
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_async_session
from schema.reservation import ReservationCreate


router2 = APIRouter()


@router2.post('/reservations/')
async def main(
    obj_in: ReservationCreate,
    session: AsyncSession = Depends(get_async_session)
    ):
    result = await room_rervation.create(obj_in, session)
    return result.year()