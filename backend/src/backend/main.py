from fastapi import FastAPI
from sqlalchemy import text

from .api.routes.queue import router as queue_router
from .db.base import Base
from .db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(queue_router)


@app.get("/")
def root():
    return {"message": "NextUp API is running"}


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}