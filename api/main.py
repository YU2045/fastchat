from fastapi import FastAPI
from api.routers import message, like

app = FastAPI()
app.include_router(message.router)
app.include_router(like.router)
