import itertools
import threading

from app.models import Item


class Store:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._ids = itertools.count(1)
        self._lock = threading.Lock()

    def add(self, title: str, created_at) -> Item:
        with self._lock:
            item = Item(id=next(self._ids), title=title, done=False, created_at=created_at)
            self._items[item.id] = item
            return item

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
            del self._items[item_id]

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._ids = itertools.count(1)


store = Store()
