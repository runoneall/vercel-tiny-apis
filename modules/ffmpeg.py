import os
import shutil
import subprocess
import tempfile

from flask import Blueprint, Flask, after_this_request, render_template, request, send_file


class Module:
    def __init__(self, app: Flask) -> None:
        router = Blueprint("ffmpeg", __name__, url_prefix="/ffmpeg")
        router.get("/")(self.webui)
        router.post("/convert")(self.convert)
        app.register_blueprint(router)

    def webui(self):
        return render_template("ffmpeg.html.j2")

    def convert(self):
        file = request.files["file"]
        output_format = request.form.get("format", "").lower().strip()
        temp_dir = tempfile.mkdtemp()

        @after_this_request
        def cleanup(response):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return response

        input_path = os.path.join(temp_dir, "input_media")
        output_path = os.path.join(temp_dir, f"output.{output_format}")

        file.save(input_path)

        command = ["bin/ffmpeg", "-y", "-i", input_path, output_path]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return send_file(output_path, as_attachment=True, download_name=f"converted.{output_format}")
