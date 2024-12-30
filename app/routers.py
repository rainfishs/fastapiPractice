"""
=== FastAPI Routers ===
"""

import hashlib
import os
from typing import Sequence

from fastapi import APIRouter, HTTPException

from .database import SessionLocal
from .models import Todo, User
from .schemas import *
from .utils import get_salt

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


"""
User Router
"""

users_router = APIRouter(tags=["User"])


# 查所有 user
@users_router.get("/users")
def read_users() -> Sequence[UserResponse]:
    with SessionLocal() as db:
        return db.query(User).all()


# 查單一 user
@users_router.get("/user/{user_id}")
def read_user(user_id: int) -> UserResponse:
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


# 新增 user
@users_router.post("/users")
def create_user(user: UserCreate):
    # Hash Password
    salt = get_salt()
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user.password.encode("utf-8"), salt, 100000
    )

    with SessionLocal() as db:
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password,
        )
        # 判斷是否有重複的 username
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"detail": "User created successfully"}


# 刪除 user
@users_router.delete("/user")
def delete_user(user: UserDelete):
    # with SessionLocal() as db:
    #     db_user = db.query(User).filter(User.id == user_id).first()
    #     if not db_user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     db.delete(db_user)
    #     db.commit()
    #     return {"detail": "User deleted successfully"}
    # Hash Password
    # salt = os.urandom(32)
    salt = get_salt()
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user.password.encode("utf-8"), salt, 100000
    )
    # if hashed_password == db_user.password_hash: # Check Password
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.id == user.id).first()
        # 驗證 db_user 所有欄位 == user 所有欄位
        user_dict = user.model_dump()
        user_dict.pop("password")
        for key, value in user_dict.items():
            if getattr(db_user, key) != value:
                raise HTTPException(
                    status_code=400, detail="User information is incorrect"
                )
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if hashed_password == db_user.password_hash:
            db.delete(db_user)
            db.commit()
            return {"detail": "User deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Password is incorrect")


# 更新 user
@users_router.put("/user/{user_id}")
def update_user(user_id: int, user: UserUpdate) -> UserResponse:
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        # 驗證密碼
        salt = get_salt()
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", user.password.encode("utf-8"), salt, 100000
        )
        if hashed_password != db_user.password_hash:
            raise HTTPException(status_code=400, detail="Password is incorrect")
        user_dict = user.model_dump()
        user_dict.pop("password")
        new_password = user_dict.pop("new_password")
        if new_password:
            hashed_new_password = hashlib.pbkdf2_hmac(
                "sha256", new_password.encode("utf-8"), salt, 100000
            )
            user_dict["password_hash"] = hashed_new_password
        for key, value in user_dict.items():
            if value:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
