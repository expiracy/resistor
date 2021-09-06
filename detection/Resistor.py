import json
import os
import numpy as np


from detection.Colours import Colours


class Resistor:

    def __init__(self, bands):

        self.bands = bands

    def order_bands(self):

        self.bands = sorted(self.bands, key=lambda resistor_band: resistor_band.bounding_rectangle.x, reverse=False)

    def remove_non_bands(self):

        heights = []

        for band in range(len(self.bands)):
            heights.append(self.bands[band].bounding_rectangle.height)

        resistor_height = max(heights)

        invalid_bands = []

        for band in range(len(self.bands)):

            if self.bands[band].bounding_rectangle.height < (resistor_height * 0.7):
                invalid_bands.append(self.bands[band])

        for index in range(len(invalid_bands)):
            self.bands.remove(invalid_bands[index])

    def type(self):

        if self.bands:
            return len(self.bands)

    def colours(self):

        colours = []
        type = self.type()

        if type == 3:
            colours = [self.bands[0].colour, self.bands[1].colour, "NONE", self.bands[2].colour, "NONE", "NONE"]

        if type == 4:
            colours = [self.bands[0].colour, self.bands[1].colour, "NONE", self.bands[2].colour,
                       self.bands[3].colour, "NONE"]

        if type == 5:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, "NONE"]

        if type == 6:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, self.bands[5].colour]

        return colours

    def get_digit_band_colours(self):
        digit_band_colours = []

        colours = self.colours()

        for index in range(3):
            if colours[index] != 'NONE':
                digit_band_colours.append(colours[index])

        return digit_band_colours

    def check_digit_band_colour_validity(self):

        digit_band_colours = self.get_digit_band_colours()

        if len(digit_band_colours) == 2:
            number_of_digit_bands = 2

        else:
            number_of_digit_bands = 3

        data_file = f'standardResistorValues{number_of_digit_bands}sf.json'

        with open(f'{os.getcwd()}\\detection\\data\\{data_file}') as valid_band_colours_list:

            valid_band_colours_list = json.load(valid_band_colours_list)

            for valid_band_colours in valid_band_colours_list:

                if valid_band_colours == digit_band_colours:
                    return True

            else:
                return False

    def identify_dupe_bands(self):
        x_list = []

        # getting x coordinate of each band and appending them to a list
        for index in range(len(self.bands)):
            x_list.append(self.bands[index].bounding_rectangle.x)

        # calculating the mean difference of the x coordinates
        np_x_list = np.array(x_list)
        difference_list = np.diff(np_x_list)
        mean_difference = np.mean(difference_list)

        dupe_band_indexes = []

        # if 2 x coordinates are less than 0.3 x the mean difference away from each other, assume it is a duplicate band
        for index in range(len(difference_list)):
            if difference_list[index] < mean_difference * 0.4:
                dupe_band_indexes.append(index)
                dupe_band_indexes.append(index + 1)

        return dupe_band_indexes

    def keep_biggest_dupe_band(self, dupe_band_indexes):
        areas = []

        for index in range(len(dupe_band_indexes)):
            areas.append(self.bands[index].bounding_rectangle.width * self.bands[index].bounding_rectangle.height)

        # I am assuming that the best colour match is the best band
        biggest_area = max(areas)
        biggest_area_index = areas.index(biggest_area)

        for index in range(len(dupe_band_indexes)):
            print(index)
            if index != biggest_area_index:
                self.bands.remove(self.bands[index])

    def flip(self):
        self.bands.reverse()

    def best_match(self):
        pass

    def main(self):

        self.remove_non_bands()
        self.order_bands()

        dupe_band_indexes = self.identify_dupe_bands()

        if dupe_band_indexes:
            self.keep_biggest_dupe_band(dupe_band_indexes)

        valid = self.check_digit_band_colour_validity()

        if not valid:
            self.flip()
            valid = self.check_digit_band_colour_validity()

            if not valid:
                self.best_match()

                return self

            else:
                return self

        else:
            return self

