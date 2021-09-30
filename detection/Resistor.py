import json
import os
import numpy as np

from detection.Colours import Colours


class Resistor:

    def __init__(self, bands):

        self.bands = bands

    def order_bands(self, reverse=False):

        self.bands = sorted(self.bands, key=lambda resistor_band: resistor_band.bounding_rectangle.x, reverse=reverse)

    def remove_non_bands(self):

        try:

            heights = [band.bounding_rectangle.height for band in self.bands]
            widths = [band.bounding_rectangle.width for band in self.bands]

            resistor_height = max(heights)
            mean_band_width = np.mean(widths)

            for band in self.bands[:]:
                if band.bounding_rectangle.height < (resistor_height * 0.3) or band.bounding_rectangle.width < (
                        mean_band_width * 0.3):
                    self.bands.remove(band)

        except:
            print("Error with getting resistor band bounding box attributes.")

    def type(self):

        if self.bands:
            return len(self.bands)

        else:
            return 6

    def colours(self):

        type = self.type()

        if type == 3:
            colours = [self.bands[0].colour, self.bands[1].colour, 'NONE', self.bands[2].colour, 'NONE', 'NONE']

        elif type == 4:
            colours = [self.bands[0].colour, self.bands[1].colour, 'NONE', self.bands[2].colour,
                       self.bands[3].colour, 'NONE']

        elif type == 5:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, 'NONE']

        elif type == 6:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, self.bands[5].colour]
        else:
            colours = ['NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE']

        return colours

    def get_digit_band_colours(self):
        digit_band_colours = []

        colours = self.colours()

        if colours:
            for index in range(3):
                if colours[index] != 'NONE':
                    digit_band_colours.append(colours[index])

            return digit_band_colours

    def standard_values(self):

        type = self.type()

        if type < 5:
            number_of_digit_bands = 2

        else:
            number_of_digit_bands = 3

        data_file = f'standardResistorValues{number_of_digit_bands}sf.json'

        with open(f'{os.path.dirname(os.path.abspath(__file__))}\\data\\{data_file}') as valid_band_colours_list:

            valid_band_colours_list = json.load(valid_band_colours_list)

            for valid_band_colours in valid_band_colours_list:
                if self.get_digit_band_colours() == valid_band_colours:
                    return True

    def main(self):

        self.remove_non_bands()
        # self.find_gold()
        self.order_bands()

        self.identify_dupe_bands()

        for band in self.bands:
            if band.dupe is True:
                self.keep_biggest_dupe_band()
                break

        valid = self.check_digit_band_colour_validity()

        if not valid:
            self.order_bands(True)
            valid = self.check_digit_band_colour_validity()

            if not valid:
                self.best_match()

                return self

            else:
                return self

        else:
            return self