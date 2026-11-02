from datetime import datetime, timezone

from app.models import Item, ItemView
from app.settings import PAGE_SIZE
from app.store import store

MAX_TITLE = 200


def clean_title(title: str) -> str:
    title = title.strip()
    if len(title) > MAX_TITLE:
        raise ValueError(f"title must be at most {MAX_TITLE} characters")
    # Titles start with a capital letter, so lists read the same way.
    return title[0].upper() + title[1:]


def create_item(title: str, due_at: datetime | None = None) -> Item:
    item = store.add(clean_title(title), datetime.now(timezone.utc))
    if due_at is None:
        return item
    if due_at.tzinfo is None:
        due_at = due_at.replace(tzinfo=timezone.utc)
    return store.update(item.model_copy(update={"due_at": due_at}))


def get_item(item_id: int) -> Item:
    return store.get(item_id)


def list_items(page: int = 1, done: bool | None = None, overdue: bool | None = None, now: datetime | None = None) -> list[Item]:
    if page < 1:
        raise ValueError("page must be 1 or more")
    items = store.list()
    if done is not None:
        items = [i for i in items if i.done == done]
    if overdue is not None:
        now = now or datetime.now(timezone.utc)
        items = [i for i in items if is_overdue(i, now) == overdue]
    start = (page - 1) * PAGE_SIZE
    return items[start : start + PAGE_SIZE]


def is_overdue(item: Item, now: datetime) -> bool:
    return item.due_at is not None and not item.done and item.due_at < now


def view(item: Item, now: datetime) -> ItemView:
    return ItemView(**item.model_dump(), overdue=is_overdue(item, now))


def complete_item(item_id: int) -> Item:
    item = store.get(item_id)
    return store.update(item.model_copy(update={"done": True}))


def delete_item(item_id: int) -> None:
    store.delete(item_id)
