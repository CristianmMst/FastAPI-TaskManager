from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.modules.users.model import UserDB
from app.modules.auth.utils import get_current_user

from app.modules.tasks.shemas import TaskCreate, TaskRead, TaskUpdate
from app.modules.tasks.services import create_task_service, delete_task_service, get_task_service, get_tasks_service, update_task_service


router = APIRouter()


@router.get("/")
def get_tasks(user: Annotated[UserDB, Depends(get_current_user)]):
    tasks = get_tasks_service(user.id)
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, user: Annotated[UserDB, Depends(get_current_user)]):
    task = get_task_service(task_id)
    return task


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, user: Annotated[UserDB, Depends(get_current_user)]):
    task = TaskCreate(title=task.title, status=task.status,
                      description=task.description, user_id=user.id)

    task_created = create_task_service(task)
    return task_created


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task: TaskUpdate, user: Annotated[UserDB, Depends(get_current_user)]):
    task_updated = update_task_service(task_id, task)
    if task_updated is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task_updated


@router.delete("/{task_id}")
def delete_task(task_id: int, user: Annotated[UserDB, Depends(get_current_user)]):
    task = delete_task_service(task_id)
    if task is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this task")
    return {"message": "Task deleted successfully"}
