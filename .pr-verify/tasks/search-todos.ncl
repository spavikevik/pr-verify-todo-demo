let pv = import "pr-verify.ncl" in
let arch = import "architecture.ncl" in
let domain = import "domain.ncl" in
let accept = import "acceptance.ncl" in
let verify = import "verification.ncl" in
pv.task {
  id = "search-todos",
  title = "Search todos by title",
  goal = "GET /todos takes q and lists only the todos whose title contains it, ignoring case.",
  context = "Paging and the done filter work as before, on the search's results.\n\nWords used here:\n"
    ++ pv.explain [domain.todo, domain.title, domain.page, arch.api, arch.service],

  promises = [
    { text = "GET /todos takes q and lists only the todos whose title contains it, ignoring case", files = [arch.api, arch.service] },
  ],

  ready = [ pv.not_yet { file = "app/main.py", find = "q: str", text = "GET /todos has no search yet" } ],
  wont = [ accept.store_unchanged, accept.no_packages ],
  done_when = [ pv.adds_tests "search", accept.changelog_says "search" ],
  by_hand = [ verify.tests, verify.try_it "GET /todos?q=MILK lists the todo \"Buy milk\" and nothing else" ],

  may_change = [arch.api, arch.service, arch.tests, arch.docs],
}
