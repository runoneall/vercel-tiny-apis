from hashlib import md5
from importlib.util import module_from_spec, spec_from_file_location
import pathlib

from flask import Flask, render_template
from flask_compress import Compress
from flask_minify import minify

app = Flask(__name__)
Compress(app)
minify(app)


@app.get("/")
def index():
    pages: list[str] = [rule.rule for rule in app.url_map.iter_rules() if rule.methods and "GET" in rule.methods and "<" not in rule.rule]
    return render_template("index.html.j2", pages=pages)


modules_dir = pathlib.Path("modules")
if modules_dir.is_file():
    modules_dir.unlink()
if not modules_dir.exists():
    modules_dir.mkdir()


class ModuleEntry:
    def __init__(self, app: Flask) -> None:
        pass


for module_file in [item for item in modules_dir.glob("*.py") if item.is_file()]:
    abs_path = module_file.absolute().__str__()
    module_name = "mod_" + md5(abs_path.encode("utf-8")).hexdigest()
    spec = spec_from_file_location(module_name, abs_path)
    if not spec or not spec.loader:
        continue

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "Module"):
        continue

    entry: type[ModuleEntry] = module.Module
    entry(app)

if __name__ == "__main__":
    app.run(debug=True)
