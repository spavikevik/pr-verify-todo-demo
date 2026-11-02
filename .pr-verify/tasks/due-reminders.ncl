let pv = import "pr-verify.ncl" in
let arch = import "architecture.ncl" in
let domain = import "domain.ncl" in
let accept = import "acceptance.ncl" in
pv.task {
  id = "due-reminders",
  title = "List what's due soon",
  goal = "GET /todos/due-soon lists the todos due in the next 24 hours that aren't done, soonest first.",
  context = "Words used here:\n" ++ pv.explain [domain.due_date, domain.done],
  promises = [ "GET /todos/due-soon lists undone todos due within 24 hours, soonest first" ],

  # Due dates come first (issue #1). Until they're on main, this task can't start.
  ready = [ pv.file_contains { file = "app/models.py", find = "due_at", text = "Todos have due dates (issue #1 is merged)" } ],
  wont = [ accept.store_unchanged, accept.no_packages ],
  done_when = [ pv.adds_tests "what's due soon" ],
  may_change = [arch.api, arch.service, arch.tests, arch.docs],
}
