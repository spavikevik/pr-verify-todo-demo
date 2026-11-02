let pv = import "pr-verify.ncl" in
let arch = import "architecture.ncl" in
let accept = import "acceptance.ncl" in
let verify = import "verification.ncl" in
pv.task {
  id = "export-csv",
  title = "Export todos as CSV",
  goal = "GET /todos/export.csv downloads every todo as CSV: id, title, done, created_at.",
  promises = [ "GET /todos/export.csv answers text/csv with a header row and one row per todo" ],
  wont = [ accept.store_unchanged, accept.no_packages, pv.no_changes_of ['concurrency] ],
  done_when = [ pv.adds_tests "the CSV export", accept.changelog_says "CSV" ],
  by_hand = [ verify.tests, verify.try_it "Open the export in a spreadsheet: a title with a comma stays one cell" ],
  may_change = [arch.api, arch.service, arch.tests, arch.docs],
}
