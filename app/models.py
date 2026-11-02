from datetime import datetime

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime


class TodoCreate(BaseModel):
    title: str


# Old name, kept so existing imports still work.
Item = Todo
