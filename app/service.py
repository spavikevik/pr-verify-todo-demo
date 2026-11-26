from datetime import datetime, timezone

from app.models import Item
from app.settings import PAGE_SIZE
from app.store import store

MAX_TITLE = 200


def clean_title(title: str) -> str:
    title = title.strip()
    if len(title) > MAX_TITLE:
        raise ValueError(f"title must be at most {MAX_TITLE} characters")
    # Titles start with a capital letter, so lists read the same way.
    return title[0].upper() + title[1:]


def clean_tags(tags: list[str]) -> list[str]:
    # Tags are compared as typed, without surrounding spaces; an empty tag is dropped.
    return sorted({t.strip().lower() for t in tags if t.strip()})


def create_item(title: str, tags: list[str] = ()) -> Item:
    return store.add(clean_title(title), datetime.now(timezone.utc), clean_tags(list(tags)))


def get_item(item_id: int) -> Item:
    return store.get(item_id)


def list_items(page: int = 1, done: bool | None = None, tag: str | None = None) -> list[Item]:
    if page < 1:
        raise ValueError("page must be 1 or more")
    items = store.with_tag(tag.strip().lower()) if tag else store.list()
    if done is not None:
        items = [i for i in items if i.done == done]
    start = (page - 1) * PAGE_SIZE
    return items[start : start + PAGE_SIZE]


def complete_item(item_id: int) -> Item:
    item = store.get(item_id)
    return store.update(item.model_copy(update={"done": True}))


def delete_item(item_id: int) -> None:
    store.delete(item_id)
