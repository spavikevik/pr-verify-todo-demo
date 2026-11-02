# Conditions the todo tasks share.
let pv = import "pr-verify.ncl" in
let arch = import "architecture.ncl" in
{
  # The store is shared by every route; a change to it gets its own PR.
  store_unchanged = pv.leaves_area arch.store & { id = "store-unchanged" },
  no_packages = pv.no_new_packages,
  # The changelog says what changed for people calling the API.
  changelog_says = fun word => pv.file_contains { file = "CHANGELOG.md", find = word, text = "The changelog mentions %{word}" },
}
