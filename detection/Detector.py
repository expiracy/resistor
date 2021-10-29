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

    # Detects the resistor bands from an image.
    def detect(self, location):
        try:
            self.image = Image().load(location)

            if self.image.width() > 1280:
                ratio = self.image.width() / self.image.height()

                scale = 1280 / ratio

                self.image.resize(1280, round(scale))

            resistor_image = ResistorLocator(self.image).locate()

            if resistor_image:

                slice_bands = SliceBandsFinder(resistor_image.clone()).main()

                possible_bands = SliceBandSelector(slice_bands).find_possible_bands()

                resistor_bands = BandIdentifier(possible_bands, slice_bands).find_resistor_bands()

                self.resistor = Resistor(resistor_bands).main()

                return self.resistor, resistor_image

            else:
                self.resistor.bands = [None, None, None, None, None, None]

                return self.resistor, self.image

        except Exception as E:
            print('Error with Detector.')
            print(E)



