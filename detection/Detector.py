from detection.BandIdentifier import BandIdentifier
from detection.Image import Image
from detection.Resistor import Resistor
from detection.ResistorLocator import ResistorLocator
from detection.SliceBandSelector import SliceBandSelector
from detection.SliceBandsFinder import SliceBandsFinder


class Detector:
    def __init__(self):
        self.image = None
        self.resistor = None

    # Resizes the image to a more processable size.
    def resize_image(self):
        try:
            if self.image.width() > 1280:
                ratio = self.image.width() / self.image.height()

                scale = 1280 / ratio

                self.image.resize(1280, round(scale))

        except:
            raise Exception("Error resizing image")

    # Detects the resistor bands from an image.
    def detect(self, location):
        try:
            self.image = Image().load(location)

            self.resize_image()

            resistor_image = ResistorLocator(self.image).locate()

            slice_bands = SliceBandsFinder(resistor_image.clone()).main()

            possible_bands = SliceBandSelector(slice_bands).find_possible_bands()

            if len(possible_bands) > 3:

                resistor_bands = BandIdentifier(possible_bands, slice_bands).find_resistor_bands()

                self.resistor = Resistor(resistor_bands).main()

                return self.resistor, resistor_image

            else:
                raise Exception("Error finding possible bands")

        except Exception as error:
            raise Exception(f'Error detecting resistor values: {error}')
