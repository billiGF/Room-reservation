from fastapi import APIRouter
from api import meetingroom_router, reservation_router

router = APIRouter()
router.include_router(meetingroom_router, tags=['MeetingRoom'], prefix='/meetingroom')
router.include_router(reservation_router, tags=['Reservation'], prefix='/reservation')