from enum import Enum

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database import get_connection


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


@router.post("/project/{project_id}", status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, task: TaskCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, status, priority, project_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            task.title,
            task.description,
            task.status.value,
            task.priority.value,
            project_id
        )
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "project_id": project_id
    }


@router.get("/project/{project_id}")
def get_tasks(project_id: int):
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE project_id = ?
        """,
        (project_id,)
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskCreate
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?, priority = ?
        WHERE id = ?
        """,
        (
            task.title,
            task.description,
            task.status.value,
            task.priority.value,
            task_id
        )
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if updated_task is None:
        raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    return dict(updated_task)


@router.delete("/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {"message": "Task deleted successfully"}