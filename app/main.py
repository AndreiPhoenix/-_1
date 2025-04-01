from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tasks, users  # изменили .api на app.api
from .auth.auth import auth_router  # относительный импорт
from app.database import engine, Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Task Management API"}
