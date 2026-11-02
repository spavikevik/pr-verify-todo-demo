from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime


class ItemCreate(BaseModel):
    title: str


class Move(BaseModel):
    before: int | None = None
