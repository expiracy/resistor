from flask import Flask, request, redirect, render_template, url_for
import requests
from os.path import join, dirname, realpath
from detection.Detector import Detector
#https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
UPLOADS_PATH = join(dirname(realpath(__file__)))
server = Flask(__name__, template_folder="resources", static_folder="resources/static/")

@server.route("/", methods=["GET", "POST"])
def index():

    data = None

    if request.method == "POST":
        file = request.files["file"]
        x = int(float(request.form["x"]))
        y = int(float(request.form["y"]))

        location = "images/" + file.filename

        with open(location, "wb") as target:
            file.save(target)

        resistance = Detector.create().detect(location, x, y)

        bands = resistance.colours

        return redirect(url_for("resistor"), code=307)
        #return render_template("ResistorBands.html", data=colours)

    else:
        return render_template("Resistor.html", data=data)

@server.route("/resistor", methods=["GET"])
def resistor(data="738294793749"):
    return render_template("Resistor.html", data=data)

if __name__ == "__main__":
    server.run()
