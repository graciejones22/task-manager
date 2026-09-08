from fastapi import APIRouter
from database import get_connection

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
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


@router.get("/")
def get_projects():
    connection = get_connection()

    projects = connection.execute(
        "SELECT * FROM projects"
    ).fetchall()

    connection.close()

    return [dict(project) for project in projects]