from flask import Flask, render_template
from flask_compress import Compress
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.config["MINIFY_PAGE"] = True

Compress(app)
HTMLMIN(app)


@app.get("/")
def index():
    pages: list[str] = [rule.rule for rule in app.url_map.iter_rules() if rule.methods and "GET" in rule.methods and "<" not in rule.rule]
    return render_template("index.html.j2", pages=pages)


if __name__ == "__main__":
    app.run(debug=True)
