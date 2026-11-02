let pv = import "pr-verify.ncl" in
let arch = import "architecture.ncl" in
let domain = import "domain.ncl" in
let accept = import "acceptance.ncl" in
let verify = import "verification.ncl" in
pv.task {
  id = "todo-tags",
  title = "Tag todos",
  goal = "A todo can have tags, and GET /todos?tag= lists only the todos with that tag.",
  context = "Tags are set when a todo is made. Filtering by tag goes with paging and the done filter.\n\nWords used here:\n"
    ++ pv.explain [domain.todo, domain.tag, arch.models, arch.service, arch.store],

  promises = [
    { text = "A todo has a list of tags, empty unless given", files = [arch.models] },
    { text = "GET /todos?tag= lists only the todos with that tag", files = [arch.api, arch.service] },
  ],

  wont = [ accept.store_unchanged, accept.no_packages ],
  done_when = [ pv.adds_tests "tags", accept.changelog_says "tag" ],
  by_hand = [ verify.tests ],

  may_change = [arch.api, arch.service, arch.models, arch.tests, arch.docs],
}
