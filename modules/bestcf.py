from flask import Blueprint, Response, render_template
import requests


class Module:
    scope = "bestcf"
    base_api = "https://bestcf.pages.dev"

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.webui)
        router.get("/<path:path>")(self.converter)

    def webui(self):
        return render_template("bestcf.html.j2")

    def converter(self, path: str):
        if not path.startswith("/"):
            path = "/" + path

        lines: list[str] = []
        resp = requests.get(url=self.base_api + path, stream=True)
        for raw_line in resp.iter_lines():
            if raw_line:
                line = raw_line.decode("utf-8")
                if "BestCF.pages.dev" in line:
                    continue

                lines.append(line.replace("|", "-"))

        return Response(
            "\n".join(lines),
            status=resp.status_code,
            content_type=resp.headers.get("content-type"),
        )
