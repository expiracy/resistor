from detection.ResistorLocator import ResistorLocator
from detection.SliceBandFinder import SliceBandFinder
from detection.Image import Image
from detection.Resistor import Resistor
from detection.BandIdentifier import BandIdentifier
from detection.SliceBandSelector import SliceBandSelector


class Detector:

    def __init__(self):
        self.image = None
        self.resistor = None

    # Detects the resistor colours from an image.
    def detect(self, location):
        try:
            self.image = Image().load(location)

            if self.image.width() > 1280:
                ratio = self.image.width() / self.image.height()

                scale = 1280 / ratio

                self.image.resize(1280, round(scale))

            resistor_image = ResistorLocator(self.image).locate()

            if resistor_image:

                slice_bands = SliceBandFinder(resistor_image.clone()).find()

                possible_bands, number_of_bands = SliceBandSelector(slice_bands).find_possible_bands()

                resistor_bands = BandIdentifier(possible_bands, slice_bands).find_resistor_bands(number_of_bands)

                self.resistor = Resistor(resistor_bands).main()

                return self.resistor, resistor_image

            else:
                self.resistor.bands = ['BLACK', 'BLACK', 'BLACK', 'BLACK', 'BLACK', 'BLACK']

                return self.resistor, self.image

        except Exception as E:
            print('Error with Detector.')
            print(E)



