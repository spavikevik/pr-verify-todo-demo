from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime
    due_at: datetime | None = None


class ItemView(Item):
    overdue: bool


class ItemCreate(BaseModel):
    title: str
    due_at: datetime | None = None
