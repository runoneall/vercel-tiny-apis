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
        path = path.replace(self.base_api, "")
        path += "/" if not path.endswith("/") else ""

        resp = requests.get(url=self.base_api + path)
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get("content-type"),
        )
