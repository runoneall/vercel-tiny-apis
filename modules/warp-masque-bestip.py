from urllib import parse

from flask import Blueprint, Response, render_template, request
import requests


class Module:
    scope = "warp-masque-bestip"
    base_api = parse.urlparse("https://warp-masque-bestip.pages.dev")

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.get)

    def get(self):
        ips = request.args.get("ips")
        level = request.args.get("level")
        port = request.args.get("port")

        if not ips:
            return render_template("warp-masque-bestip.html.j2")

        query_params: dict[str, str | None] = {
            "ips": ips,
            "level": level,
            "port": port,
        }

        filtered_params = {k: v for k, v in query_params.items() if v is not None and v != ""}
        query = parse.urlencode(filtered_params)
        url = self.base_api._replace(query=query).geturl()

        lines: list[str] = []
        resp = requests.get(url=url, stream=True)
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
