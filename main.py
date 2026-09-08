from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from database import create_tables, get_connection

app = FastAPI()

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


create_tables()


@app.get("/")
def home():
    return {"message": "Welcome to Manager!"}


@app.post("/projects")
def create_project(name: str, description: str = ""):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO projects (name, description)
        VALUES (?, ?)
        """,
        (name, description)
    )

    connection.commit()

    project_id = cursor.lastrowid

    connection.close()

    return {
        "id": project_id,
        "name": name,
        "description": description
    }


@app.get("/projects")
def get_projects():
    connection = get_connection()

    projects = connection.execute(
        "SELECT * FROM projects"
    ).fetchall()

    connection.close()

    return [dict(project) for project in projects]

@app.post("/projects/{project_id}/tasks")
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
            task.status,
            task.priority,
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


@app.get("/projects/{project_id}/tasks")
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

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str,
    description: str = "",
    status: str = "To Do",
    priority: str = "Medium"
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?, priority = ?
        WHERE id = ?
        """,
        (title, description, status, priority, task_id)
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if updated_task is None:
        return {"error": "Task not found"}

    return dict(updated_task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {"message": "Task deleted successfully"}