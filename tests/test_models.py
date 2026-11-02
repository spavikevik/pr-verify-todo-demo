from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models import Item, ItemCreate


def test_item_holds_its_fields():
    now = datetime.now(timezone.utc)
    item = Item(id=1, title="Buy milk", done=False, created_at=now)
    assert (item.id, item.title, item.done, item.created_at) == (1, "Buy milk", False, now)


def test_item_requires_all_fields():
    with pytest.raises(ValidationError):
        Item(id=1, title="Buy milk")


def test_item_coerces_numeric_strings_to_int():
    item = Item(id="7", title="x", done=False, created_at="2026-01-01T00:00:00Z")
    assert item.id == 7


def test_item_create_needs_a_title():
    with pytest.raises(ValidationError):
        ItemCreate()


def test_item_create_keeps_title_as_given():
    assert ItemCreate(title="  padded ").title == "  padded "
