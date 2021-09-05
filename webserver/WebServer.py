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

    file = request.files["file"]

    location = f'{os.getcwd()}\\images\\{file.filename}'

    location = os.path.abspath(location)

    with open(location, "wb") as target:
        file.save(target)

    resistor = Detector.create().detect(location)

    print(resistor.colours)

    return jsonify(colours=resistor.colours(), type=resistor.type())



if __name__ == "__main__":
    app.run()
