import os.path
import json
from flask import Flask, request, render_template, jsonify
from os.path import join, dirname, realpath
from detection.Detector import Detector
from detection.Resistor import Resistor
from detection.ResistorBand import ResistorBand

UPLOADS_PATH = join(dirname(realpath(__file__)))
app = Flask(__name__, template_folder='resources', static_folder='resources/static/')


# Returns the UI of the page.
@app.route('/ui', methods=['GET'])
def ui():
    return render_template('Resistor.html')


# Calls the detector program.
@app.route('/api/detect', methods=['POST'])
def detect():

    resistor_type = None

    file = request.files['file']

    if request.values:
        resistor_type = request.values['type']

    location = f'{os.getcwd()}\\images\\{file.filename}'

    location = os.path.abspath(location)
    try:
        with open(location, 'wb') as target:
            file.save(target)

        resistor, resistor_image = Detector().detect(location)

        resistor_image_byte_stream = resistor_image.byte_stream()

        resistor_image_byte_stream = resistor_image_byte_stream.decode('utf-8')

        resistor_colours = resistor.colours()
        print(resistor_colours)

        if resistor_type is None:
            resistor_type = resistor.type()

        return jsonify(colours=resistor_colours, type=resistor_type, image=resistor_image_byte_stream, valid=resistor.valid)

    except Exception as E:
        print(E)

        colours = [None, None, None, None, None, None]

        if resistor_type is None:
            resistor_type = 6

        return jsonify(colours=colours, type=resistor_type, image=None, valid=False)


@app.route('/api/validate', methods=['POST'])
def validate():
    resistor_bands_colours = request.values["resistor_bands"]

    resistor_bands_colours = json.loads(resistor_bands_colours)

    resistor_bands = []

    for resistor_band in resistor_bands_colours:
        if resistor_band is not None:
            resistor_bands.append(ResistorBand(resistor_band))

    valid = Resistor(resistor_bands).check_valid()

    return jsonify(valid=valid)


if __name__ == '__main__':
    app.run()
