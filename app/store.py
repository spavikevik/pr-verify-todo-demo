import itertools
import threading

from app.models import Item


class Store:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._by_tag: dict[str, set[int]] = {}
        self._ids = itertools.count(1)
        self._lock = threading.Lock()

    def add(self, title: str, created_at, tags: list[str] = ()) -> Item:
        with self._lock:
            item = Item(id=next(self._ids), title=title, done=False, created_at=created_at, tags=list(tags))
            self._items[item.id] = item
            for tag in item.tags:
                self._by_tag.setdefault(tag, set()).add(item.id)
            return item

    def with_tag(self, tag: str) -> list[Item]:
        with self._lock:
            return sorted((self._items[i] for i in self._by_tag.get(tag, ())), key=lambda i: i.id)

    def get(self, item_id: int) -> Item:
        with self._lock:
            return self._items[item_id]

    def list(self) -> list[Item]:
        with self._lock:
            return sorted(self._items.values(), key=lambda i: i.id)

    def update(self, item: Item) -> Item:
        with self._lock:
            if item.id not in self._items:
                raise KeyError(item.id)
            self._items[item.id] = item
            return item

    def delete(self, item_id: int) -> None:
        with self._lock:
            item = self._items.pop(item_id)
            for tag in item.tags:
                self._by_tag.get(tag, set()).discard(item_id)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._by_tag.clear()
            self._ids = itertools.count(1)


store = Store()
