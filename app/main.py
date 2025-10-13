import uvicorn
from fastapi import FastAPI
from core.config import settings
from api.routers import main_router

app = FastAPI(title=settings.app_title, description='You can reserv rooms')
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    