"""
=== Pydantic Models (Schemas) ===
for validation, parsing data in request and response
"""

from pydantic import BaseModel, Field


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
