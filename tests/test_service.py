import threading

import pytest

from app import service
from app.settings import PAGE_SIZE
from app.store import store


def test_create_strips_the_title():
    assert service.create_item("  Buy milk  ").title == "Buy milk"


def test_create_stamps_a_timezone_aware_time():
    assert service.create_item("a").created_at.tzinfo is not None


def test_create_assigns_increasing_ids():
    assert [service.create_item(t).id for t in "abc"] == [1, 2, 3]


def test_create_rejects_a_long_title():
    with pytest.raises(ValueError):
        service.create_item("x" * 201)


def test_create_capitalizes_the_title():
    assert service.create_item("buy milk").title == "Buy milk"


def test_create_accepts_the_longest_title():
    assert len(service.create_item("x" * 200).title) == 200


def test_get_unknown_item_raises_key_error():
    with pytest.raises(KeyError):
        service.get_item(99)


def test_complete_marks_the_item_done():
    item = service.create_item("a")
    assert service.complete_item(item.id).done is True
    assert service.get_item(item.id).done is True


def test_complete_unknown_item_raises_key_error():
    with pytest.raises(KeyError):
        service.complete_item(99)


def test_delete_removes_the_item():
    item = service.create_item("a")
    service.delete_item(item.id)
    assert service.list_items() == []


def test_delete_unknown_item_raises_key_error():
    with pytest.raises(KeyError):
        service.delete_item(99)


def test_list_is_paged():
    for n in range(PAGE_SIZE + 5):
        service.create_item(f"t{n}")
    assert len(service.list_items(1)) == PAGE_SIZE
    assert len(service.list_items(2)) == 5
    assert service.list_items(3) == []


def test_list_rejects_page_zero():
    with pytest.raises(ValueError):
        service.list_items(0)


def test_list_filters_by_done():
    first = service.create_item("a")
    service.create_item("b")
    service.complete_item(first.id)
    assert [i.title for i in service.list_items(done=True)] == ["A"]
    assert [i.title for i in service.list_items(done=False)] == ["B"]


def test_store_update_unknown_item_raises_key_error():
    item = service.create_item("a")
    store.delete(item.id)
    with pytest.raises(KeyError):
        store.update(item)


def test_concurrent_creates_get_distinct_ids():
    ids: list[int] = []
    threads = [threading.Thread(target=lambda: ids.append(service.create_item("a").id)) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(ids) == list(range(1, 21))


def test_search_ignores_case():
    service.create_item("Buy milk")
    service.create_item("Walk the dog")
    assert [i.title for i in service.list_items(q="MILK")] == ["Buy milk"]


def test_search_and_done_filter_combine():
    a = service.create_item("Buy milk")
    service.create_item("Buy bread")
    service.complete_item(a.id)
    assert [i.title for i in service.list_items(done=False, q="buy")] == ["Buy bread"]


def test_an_empty_search_lists_everything():
    service.create_item("a")
    service.create_item("b")
    assert len(service.list_items(q="")) == 2
