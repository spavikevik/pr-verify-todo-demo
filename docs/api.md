# API examples

Every route takes and returns JSON. Times are UTC, in ISO 8601.

## Create a todo

```http
POST /todos
{"title": "Buy milk"}
```

`201 Created`:

```json
{"id": 1, "title": "Buy milk", "done": false, "created_at": "2026-11-02T09:00:00Z"}
```

A blank title, or one over 200 characters, gives `422` with a `detail` message.

## List todos

```http
GET /todos?page=1&done=false
```

`200 OK`, at most 20 per page, oldest first:

```json
[{"id": 1, "title": "Buy milk", "done": false, "created_at": "2026-11-02T09:00:00Z"}]
```

## Get one todo

```http
GET /todos/1
```

`200 OK` with the todo, or `404` with `{"detail": "todo not found"}`.

## Complete a todo

```http
POST /todos/1/complete
```

`200 OK` with the todo, now `"done": true`, or `404`.

## Delete a todo

```http
DELETE /todos/1
```

`204 No Content`, or `404`.
