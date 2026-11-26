from fastapi import FastAPI, HTTPException

from app import service
from app.models import Item, ItemCreate

app = FastAPI(title="Todo demo")


@app.get("/todos")
def list_todos(page: int = 1, done: bool | None = None, q: str | None = None) -> list[Item]:
    try:
        return service.list_items(page, done, q)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="todo not found")


@app.post("/todos", status_code=201)
def create_todo(body: ItemCreate) -> Item:
    try:
        return service.create_item(body.title)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="todo not found")


@app.get("/todos/{item_id}")
def get_todo(item_id: int) -> Item:
    try:
        return service.get_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="todo not found")


@app.post("/todos/{item_id}/complete")
def complete_todo(item_id: int) -> Item:
    try:
        return service.complete_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="todo not found")


@app.delete("/todos/{item_id}", status_code=204)
def delete_todo(item_id: int) -> None:
    try:
        service.delete_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="todo not found")
