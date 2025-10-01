import uvicorn
from fastapi import FastAPI
from core.config import settings
from api.meeting_room import router

app = FastAPI(title=settings.app_title, description='You can reserv rooms')
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
