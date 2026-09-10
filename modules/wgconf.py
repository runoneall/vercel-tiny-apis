import os
import shutil
import tempfile

from flask import Blueprint, after_this_request, render_template, request, send_file
import wgconfig


class Module:
    scope = "wgconf"

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.webui)
        router.post("/gen")(self.gen)

    def webui(self):
        return render_template("wgconf.html.j2")

    def gen(self):
        file = request.files["file"]
        ipv4 = request.form.get("ipv4")
        ipv6 = request.form.get("ipv6")

        temp_dir = tempfile.mkdtemp()
        wc_file_name = "wg.conf"
        wc_file = os.path.join(temp_dir, wc_file_name)
        file.save(wc_file)

        @after_this_request
        def cleanup(response):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return response

        wc = wgconfig.WGConfig(wc_file)
        wc.read_file()

        if ipv4:
            wc.add_attr(None, "PostUp", f"ip -4 rule add from {ipv4} lookup main")
            wc.add_attr(None, "PostDown", f"ip -4 rule delete from {ipv4} lookup main")

        if ipv6:
            wc.add_attr(None, "PostUp", f"ip -6 rule add from {ipv6} lookup main")
            wc.add_attr(None, "PostDown", f"ip -6 rule delete from {ipv6} lookup main")

        wc.write_file()
        return send_file(wc_file, as_attachment=True, download_name=wc_file_name)
