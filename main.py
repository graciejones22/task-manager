from fastapi import FastAPI
from database import create_tables, get_connection

app = FastAPI()

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
def create_task(
    project_id: int,
    title: str,
    description: str = "",
    priority: str = "Medium"
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, priority, project_id)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, priority, project_id)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
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