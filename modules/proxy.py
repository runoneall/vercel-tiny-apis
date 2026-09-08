from flask import Blueprint, Response, render_template, request, stream_with_context
import requests


class Module:
    scope = "proxy"

    def __init__(self, router: Blueprint) -> None:
        router.route("/", methods=["GET", "POST", "PUT", "DELETE"])(self.proxy)

    def proxy(self):
        url = request.args.get("url")
        if not url:
            return render_template("proxy.html.j2")

        req_headers = {k: v for k, v in request.headers if k.lower() != "host"}
        resp = requests.request(
            method=request.method,
            url=url,
            headers=req_headers,
            data=request.get_data(),
            params=request.args,
            stream=True,
        )

        def generate():
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]
        return Response(
            stream_with_context(generate()),
            status=resp.status_code,
            headers=headers,
            content_type=resp.headers.get("content-type"),
        )
