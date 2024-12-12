from fastapi import FastAPI

from .routers import todos_router

app = FastAPI()

app.include_router(todos_router, prefix="/api")
