from detection.BandIdentifier import BandIdentifier
from detection.Image import Image
from detection.Resistor import Resistor
from detection.ResistorLocator import ResistorLocator
from detection.SliceBandsFilter import SliceBandsFilter
from detection.SliceBandsFinder import SliceBandsFinder


# The main class of the program, responsible for managing the operation of the other classes.
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
    def detect(self, location, maximum_band_count):
        try:
            self.image = Image().load(location)

            self.resize_image()

            resistor_image = ResistorLocator(self.image).locate()

            # resistor_image.show()

            slice_bands = SliceBandsFinder(resistor_image.clone()).find_all_bands()

            # print('Original Detected Bands')
            # print(str(slice_bands))

            slice_band_filter = SliceBandsFilter(slice_bands)

            slice_band_filter.remove_short_bands()

            slice_band_filter.remove_narrow_bands()

            # print('Slice bands after removing narrow')
            # print(str(slice_bands))

            # band_count = slice_bands.get_band_group_count()
            # print(f'Predicted bands count={band_count}')

            possible_bands = slice_band_filter.find_possible_bands(maximum_band_count)

            # print('Possible bands using k-means')
            # print(str(possible_bands))

            if 3 <= len(possible_bands.groups()) <= 6:

                resistor_bands = BandIdentifier(possible_bands).find_resistor_bands()

                self.resistor = Resistor(resistor_bands).main()

                return self.resistor, resistor_image

            else:
                raise Exception('Not enough bands were located')

        except Exception as error:
            print(error)
            raise Exception(f'Error detecting resistor values: {error}')
