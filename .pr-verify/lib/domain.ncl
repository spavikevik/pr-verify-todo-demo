# The todo app's words, for a task's context: pv.explain [domain.todo, domain.page].
let pv = import "pr-verify.ncl" in
{
  todo = pv.term "todo" "One thing to do: an id, a title, a done flag and when it was made. The code calls it Item.",
  title = pv.term "title" "A todo's text: trimmed, at most 200 characters, starting with a capital letter.",
  done = pv.term "done" "A todo that was completed. GET /todos?done=true lists only those.",
  page = pv.term "page" "GET /todos lists 20 todos at a time (PAGE_SIZE); ?page= starts at 1.",
  tag = pv.term "tag" "A short word on a todo, such as home or work. A todo has any number of them.",
  due_date = pv.term "due date" "When a todo should be done by. Optional; added by the due dates work (issue #1).",
}
