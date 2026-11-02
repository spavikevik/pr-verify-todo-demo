This repository is staged to demonstrate pr-verify: its issues, plans and pull requests were written to show what pr-verify finds.

# todo-demo

A small todo API built with FastAPI. The domain model is `Item`: an id, a title, a done flag and a creation time.

## Run it

```bash
uv sync
uv run pytest
uv run fastapi dev app/main.py
```

Routes: `GET /todos` (paged, `?done=true|false`), `POST /todos`, `GET /todos/{id}`, `POST /todos/{id}/complete`, `DELETE /todos/{id}`.
