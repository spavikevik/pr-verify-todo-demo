from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime
    tags: list[str] = []


class ItemCreate(BaseModel):
    title: str
    tags: list[str] = []
