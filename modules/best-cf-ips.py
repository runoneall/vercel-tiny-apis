from flask import Blueprint, Response, render_template
import requests


class Module:
    scope = "best-cf-ips"
    base_api = "https://raw.githubusercontent.com/LancelotRar/best-cf-ips/main"

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.webui)
        router.get("/<string:file>")(self.get)

    def webui(self):
        return render_template("best-cf-ips.html.j2")

    def get(self, file: str):
        if file == "all":
            file = "/best-cf-ip-collected.txt"

        if file.startswith("top"):
            file = "/best-cf-ip-scanned-" + file + ".txt"

        lines: list[str] = []
        resp = requests.get(url=self.base_api + file, stream=True)
        for raw_line in resp.iter_lines():
            if raw_line:
                line = raw_line.decode("utf-8")
                if "best ips collected" in line or "best cf ips scanned" in line:
                    continue

                lines.append(line.replace("|", "-"))

        return Response(
            "\n".join(lines),
            status=resp.status_code,
            content_type=resp.headers.get("content-type"),
        )
