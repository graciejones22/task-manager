from enum import Enum

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.task_service import (
    create_task,
    get_tasks_for_project,
    update_task,
    delete_task
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


class TaskStatus(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM


@router.post(
    "/project/{project_id}",
    status_code=status.HTTP_201_CREATED
)
def create_new_task(project_id: int, task: TaskCreate):
    return create_task(project_id, task)


@router.get("/project/{project_id}")
def get_project_tasks(project_id: int):
    return get_tasks_for_project(project_id)


@router.put("/{task_id}")
def update_existing_task(task_id: int, task: TaskCreate):
    updated_task = update_task(task_id, task)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}")
def delete_existing_task(task_id: int):
    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}