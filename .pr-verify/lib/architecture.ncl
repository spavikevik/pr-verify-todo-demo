# The todo app's parts, by name. Tasks say "the store", not app/store.py.
let pv = import "pr-verify.ncl" in
{
  api = pv.area { name = "the API", paths = ["app/main.py"], about = "FastAPI routes. A ValueError is a 422 and a KeyError a 404." },
  service = pv.area { name = "the service", paths = ["app/service.py"], about = "The rules: titles are cleaned, pages start at 1." },
  store = pv.area { name = "the store", paths = ["app/store.py"], about = "In memory, behind one lock. Changing it needs a test and a second look." },
  models = pv.area { name = "the models", paths = ["app/models.py"], about = "Pydantic models; what the API returns." },
  settings = pv.area { name = "the settings", paths = ["app/settings.py"] },
  tests = pv.area { name = "the tests", paths = ["tests/**"] },
  docs = pv.area { name = "the docs", paths = ["README.md", "CHANGELOG.md", "docs/**"] },
  packages = pv.area { name = "the packages", paths = ["pyproject.toml", "uv.lock"] },
}
