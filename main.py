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