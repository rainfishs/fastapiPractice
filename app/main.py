from fastapi import FastAPI

from .database import Base, engine
from .routers import todos_router

app = FastAPI()

# Initialize Database's Table
Base.metadata.create_all(bind=engine)

app.include_router(todos_router, prefix="/api")
