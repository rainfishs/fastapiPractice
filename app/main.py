from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException

from .database import SessionLocal
from .models import Todo

"""=== Pydantic Models ==="""  # for validation, parsing data in request and response


class TodoSchema(BaseModel):
    title: str = Field(examples=["Buy Milk"], min_length=1)
    description: str | None = Field(
        None, examples=["Go to the store and buy some milk"], min_length=1
    )
    completed: bool = False


class TodoCreate(TodoSchema):
    pass


class TodoResponse(TodoSchema):
    id: int

    class Config:
        from_attributes = True


"""=== Routes ==="""

app = FastAPI()


# 查所有 todo
@app.get("/todos")
def read_todos() -> list[TodoResponse]:
    with SessionLocal() as db:
        return db.query(Todo).all()


# 查單一 todo
@app.get("/todo/{todo_id}")
def read_todo(todo_id: int) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return db_todo


# 新增 todo
@app.post("/todos")
def create_todo(todo: TodoCreate) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo


# 更新 todo
@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate) -> TodoResponse:
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, details="Todo not found")
        for key, value in todo.model_dump().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        return db_todo


# 刪除 todo
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, details="Todo not found")
        db.delete(db_todo)
        db.commit()
        return {"detail": "Todo deleted successfully"}
