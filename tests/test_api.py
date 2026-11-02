import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settings import PAGE_SIZE

client = TestClient(app)


def make(title="Buy milk"):
    return client.post("/todos", json={"title": title})


def test_create_returns_201_and_the_item():
    r = make()
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"
    assert r.json()["done"] is False


def test_create_without_title_is_422():
    assert client.post("/todos", json={}).status_code == 422


def test_get_returns_the_item():
    made = make().json()
    assert client.get(f"/todos/{made['id']}").json() == made


def test_get_unknown_is_404():
    assert client.get("/todos/99").status_code == 404


def test_complete_marks_done():
    made = make().json()
    r = client.post(f"/todos/{made['id']}/complete")
    assert r.status_code == 200
    assert r.json()["done"] is True


def test_complete_unknown_is_404():
    assert client.post("/todos/99/complete").status_code == 404


def test_delete_then_get_is_404():
    made = make().json()
    assert client.delete(f"/todos/{made['id']}").status_code == 204
    assert client.get(f"/todos/{made['id']}").status_code == 404


def test_delete_unknown_is_404():
    assert client.delete("/todos/99").status_code == 404


def test_list_is_paged():
    for n in range(PAGE_SIZE + 1):
        make(f"t{n}")
    assert len(client.get("/todos").json()) == PAGE_SIZE
    assert len(client.get("/todos?page=2").json()) == 1


def test_list_page_zero_is_422():
    assert client.get("/todos?page=0").status_code == 422


@pytest.mark.parametrize("flag,expected", [("true", ["A"]), ("false", ["B"])])
def test_list_filters_by_done(flag, expected):
    a = make("a").json()
    make("b")
    client.post(f"/todos/{a['id']}/complete")
    r = client.get(f"/todos?done={flag}")
    assert [i["title"] for i in r.json()] == expected
