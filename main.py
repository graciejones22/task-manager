from fastapi import FastAPI

from database import create_tables
from routers import projects, tasks


app = FastAPI(
    title="Manager API",
    description="A project and task management API",
    version="1.0.0"
)


create_tables()


app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Welcome to Manager!"}