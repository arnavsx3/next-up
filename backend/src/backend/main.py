from fastapi import FastAPI
from sqlalchemy import text

from .db.database import engine

app = FastAPI()


@app.get("/")
def root():
    return {"message": "NextUp API is running"}


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}