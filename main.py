from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from routers import projects, tasks

app = FastAPI(
    title="Manager API",
    description="A project and task management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_tables()


app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Welcome to Manager!"}