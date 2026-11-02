# Checks a person runs before merging.
let pv = import "pr-verify.ncl" in
{
  tests = pv.check { id = "pytest", text = "The tests pass", command = "uv run pytest" },
  try_it = fun what => pv.check { text = what },
}
