from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import Task, TaskCreate
from app.crud import task as crud_task
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return crud_task.create_task(db=db, task=task, user_id=current_user["id"])

@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = crud_task.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_task = crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_task = crud_task.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=Task)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_task = crud_task.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
