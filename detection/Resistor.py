import json
import os
import numpy as np

from detection.Colours import Colours


class Resistor:

    def __init__(self, bands):

        self.bands = bands

    def type(self):
        if self.bands:
            return len(self.bands)

        else:
            return 6

    def colours(self):

        type = self.type()

        if type == 3:
            colours = [self.bands[0], self.bands[1], 'NONE', self.bands[2], 'NONE', 'NONE']

        elif type == 4:
            colours = [self.bands[0], self.bands[1], 'NONE', self.bands[2],
                       self.bands[3], 'NONE']

        elif type == 5:
            colours = [self.bands[0], self.bands[1], self.bands[2], self.bands[3],
                       self.bands[4], 'NONE']

        elif type == 6:
            colours = [self.bands[0], self.bands[1], self.bands[2], self.bands[3],
                       self.bands[4], self.bands[5]]
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

    def check_valid(self, flip=False):

        if flip is True:
            self.bands = self.bands[::-1]

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

            else:
                return False

    def main(self):

        try:

            non_flip_valid = self.check_valid(flip=False)

            if non_flip_valid is True:
                return self

            else:
                flip_valid = self.check_valid(flip=True)

                if flip_valid is True:
                    return self

                else:
                    self.bands = self.bands[::-1]
                    return self

        except:
            print("Error with Resistor.")

            return self






