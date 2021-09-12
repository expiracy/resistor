import os.path

from flask import Flask, request, render_template, jsonify
from os.path import join, dirname, realpath
from detection.Detector import Detector

# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
UPLOADS_PATH = join(dirname(realpath(__file__)))
app = Flask(__name__, template_folder="resources", static_folder="resources/static/")


@app.route("/ui", methods=["GET"])
def ui():
    return render_template("Resistor.html")


@app.route("/api", methods=["POST"])
def api():
    resistor_type = None

    file = request.files["file"]

    if request.values:
        resistor_type = request.values["type"]

    location = f'{os.getcwd()}\\images\\{file.filename}'

    location = os.path.abspath(location)

    with open(location, "wb") as target:
        file.save(target)

    resistor, resistor_image = Detector.create().detect(location)

    resistor_colours = resistor.colours()

    if resistor_type is None:
        resistor_type = resistor.type()

    resistor_image_byte_stream = resistor_image.byte_stream()

    resistor_image_byte_stream = resistor_image_byte_stream.decode("utf-8")

    return jsonify(colours=resistor_colours, type=resistor_type, image=resistor_image_byte_stream)


if __name__ == "__main__":
    app.run()
