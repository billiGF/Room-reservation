import uvicorn
from fastapi import FastAPI
from core.config import settings
from api.meeting_room import router
from api.reservation import router2

app = FastAPI(title=settings.app_title, description='You can reserv rooms')
app.include_router(router, tags=['MeetingRoom'])
app.include_router(router2, tags=['Reservation'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
