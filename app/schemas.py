"""
=== Pydantic Models (Schemas) ===
for validation, parsing data in request and response
"""

from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


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


"""
User Schema
"""


class UserSchema(BaseModel):
    username: str = Field(examples=["john_doe"], min_length=3)
    email: EmailStr = Field(examples=["John_doe@gmail.com"], min_length=6)


class UserCreate(UserSchema):
    password: str = Field(examples=["password"], min_length=8)


class UserResponse(UserSchema):
    id: int
    status: bool

    class Config:
        from_attributes = True


class UserDelete(UserSchema):
    id: int
    password: str = Field(examples=["password"], min_length=8)
