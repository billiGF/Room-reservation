from fastapi import APIRouter
from api import meetingroom_router, reservation_router, user_router

main_router = APIRouter()
main_router.include_router(meetingroom_router, tags=['MeetingRoom'], prefix='/meetingroom')
main_router.include_router(reservation_router, tags=['Reservation'], prefix='/reservation')
main_router.include_router(user_router) 