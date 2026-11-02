import pytest

from app.store import store


@pytest.fixture(autouse=True)
def fresh_store():
    store.clear()
    yield
    store.clear()
