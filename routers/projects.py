from fastapi import APIRouter, status

from services.project_service import (
    create_project,
    get_all_projects
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_project(name: str, description: str = ""):
    return create_project(name, description)


@router.get("/")
def get_projects():
    return get_all_projects()