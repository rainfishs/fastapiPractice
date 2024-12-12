"""
=== FastAPI Routers ===
"""

from typing import Sequence

from fastapi import APIRouter, HTTPException

from .database import SessionLocal
from .models import Todo
from .schemas import TodoCreate, TodoResponse

todos_router = APIRouter(tags=["Todo"])


# 查所有 todo
@todos_router.get("/todos")
def read_todos() -> Sequence[TodoResponse]:
    with SessionLocal() as db:
        return db.query(Todo).all()


# 查單一 todo
@todos_router.get("/todo/{todo_id}")
def read_todo(todo_id: int) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return db_todo


# 新增 todo
@todos_router.post("/todos")
def create_todo(todo: TodoCreate) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo


# 更新 todo
@todos_router.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        for key, value in todo.model_dump().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        return db_todo


# 刪除 todo
@todos_router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(db_todo)
        db.commit()
        return {"detail": "Todo deleted successfully"}
