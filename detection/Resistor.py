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

            if self.bands[band].bounding_rectangle.height < (resistor_height * 0.4):
                invalid_bands.append(self.bands[band])

        for index in range(len(invalid_bands)):
            self.bands.remove(invalid_bands[index])

    def type(self):

        if self.bands:
            return len(self.bands)

    def colours(self):

        colours = []
        type = self.type()

        if type == 2:
            colours = [self.bands[0].colour, self.bands[1].colour, "NONE", self.bands[1].colour, "NONE", "NONE"]
            print("INVALID")

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

        if colours:

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

        with open(f'{os.path.dirname(os.path.abspath(__file__))}\\data\\{data_file}') as valid_band_colours_list:

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
        mean_difference, difference_list = self.differences(x_list)

        dupe_band_indexes = []

        # if 2 x coordinates are less than 0.4 x the mean difference away from each other, assume it is a duplicate band
        for index in range(len(difference_list)):
            if difference_list[index] < mean_difference * 0.4:
                dupe_band_indexes.append(index)
                dupe_band_indexes.append(index + 1)

        return dupe_band_indexes

    def differences(self, list):
        np_list = np.array(list)
        difference_list = np.diff(np_list)
        mean_difference = np.mean(difference_list)

        return mean_difference, difference_list

    def keep_biggest_dupe_band(self, dupe_band_indexes):
        print(dupe_band_indexes)

        areas = []

        for index in dupe_band_indexes:
            areas.append(self.bands[index].bounding_rectangle.width * self.bands[index].bounding_rectangle.height)

        # I am assuming that the best colour match is the best band
        biggest_area = max(areas)
        biggest_area_index = areas.index(biggest_area)

        dupe_bands = []

        for index in range(len(self.bands)):
            if index != biggest_area_index:
                dupe_bands.append(self.bands[index])

        for dupe_band in dupe_bands:
            self.bands.remove(dupe_band)

    def flip(self):
        self.bands.reverse()

    def best_match(self):
        pass

    def find_gold(self):

        gold_x_list = []
        x_list = []

        for band in range(len(self.bands)):
            if self.bands[band].colour == 'GOLD':
                gold_x_list.append(self.bands[band].bounding_rectangle.x)

            else:
                x_list.append(self.bands[band].bounding_rectangle.x)

        mean_difference, difference_list = self.differences(x_list)

        gold_x_false_positives = []

        for x in x_list:
            for gold_x in gold_x_list:
                if (x + (mean_difference * 0.3)) < gold_x < (x - (mean_difference * 0.3)):
                    gold_x_false_positives.append(gold_x)

        gold_bands_false_positives = []

        for band in range(len(self.bands)):
            if self.bands[band].bounding_rectangle.x in gold_x_false_positives:
                gold_bands_false_positives.append(self.bands[band])

        for band in gold_bands_false_positives:
            self.bands.remove(band)

    def main(self):

        self.remove_non_bands()
        self.find_gold()
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





