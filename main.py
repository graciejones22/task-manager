from fastapi import FastAPI
from database import create_tables

app = FastAPI()

create_tables()


@app.get("/")
def home():
    return {"message": "Welcome to Manager!"}