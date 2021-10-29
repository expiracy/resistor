from detection.ResistorLocator import ResistorLocator
from detection.SliceBandsFinder import SliceBandsFinder
from detection.Image import Image
from detection.Resistor import Resistor
from detection.BandIdentifier import BandIdentifier
from detection.SliceBandSelector import SliceBandSelector


class Detector:
    def __init__(self):
        self.image = None
        self.resistor = None

    # Resizes the image to a more processable size.
    def resize_image(self):
        if self.image.width() > 1280:
            ratio = self.image.width() / self.image.height()

            scale = 1280 / ratio

            self.image.resize(1280, round(scale))

    # Detects the resistor bands from an image.
    def detect(self, location):

        self.image = Image().load(location)

        self.resize_image()

        resistor_image = ResistorLocator(self.image).locate()

        slice_bands = SliceBandsFinder(resistor_image.clone()).main()

        possible_bands = SliceBandSelector(slice_bands).find_possible_bands()

        resistor_bands = BandIdentifier(possible_bands, slice_bands).find_resistor_bands()

        if resistor_bands:

            self.resistor = Resistor(resistor_bands).main()

            return self.resistor, resistor_image

        else:
            return None, None



