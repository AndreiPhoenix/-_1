from fastapi import FastAPI
from .database import engine
from . import models
from .routers import tasks, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Welcome to Task Manager API"}
