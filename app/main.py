from fastapi import Depends, FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

"""=== Database ==="""

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)


# Define Tables(Models)
Base = declarative_base()
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Initialize Database's Table
Base.metadata.create_all(bind=engine)

#factory method
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""=== Pydantic Models ===""" #for validation, parsing data in request and response
class Item(BaseModel):
    def __init__(self, name: str, price: float, description: str = None):
        self.name = name
        self.price = price
        self.description = description

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    
    class Config:
        from_attributes = True


"""=== Routes ==="""

app = FastAPI()

# 查所有 todo
@app.get("/todos", response_model=list[TodoResponse])
def read_todos():
    with SessionLocal() as db:
        return db.query(Todo).all()

# 查單一 todo
@app.get("/todo/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int):
    with SessionLocal() as db:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, details="Todo not found")
        return db_todo

# 新增 todo
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    with SessionLocal() as db:
        db_todo = Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

# 更新 todo
@app.put("/todo/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate):
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
