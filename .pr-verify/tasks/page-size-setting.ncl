# Written without a single path: the agent places the work, and the conditions are about meaning.
let pv = import "pr-verify.ncl" in
let accept = import "acceptance.ncl" in
pv.task {
  id = "page-size-setting",
  title = "Page size from the environment",
  goal = "TODO_PAGE_SIZE sets how many todos a page lists; without it, 20 as today.",
  promises = [ "The page size comes from TODO_PAGE_SIZE when it is set", "A page size below 1 or above 100 stops the app at start-up" ],
  wont = [ pv.no_public_api_changes, accept.no_packages, accept.store_unchanged ],
  done_when = [ pv.adds_tests "the page size" ],
}
