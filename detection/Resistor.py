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

        heights = [band.bounding_rectangle.height for band in self.bands]
        widths = [band.bounding_rectangle.width for band in self.bands]

        resistor_height = max(heights)
        mean_band_width = np.mean(widths)

        for band in self.bands[:]:
            if band.bounding_rectangle.height < (resistor_height * 0.3) or band.bounding_rectangle.width < (mean_band_width * 0.3):
                self.bands.remove(band)

    def type(self):

        if self.bands:
            return len(self.bands)

    def colours(self):

        colours = []
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
        # getting x coordinate of each band and appending them to a list
        x_list = [band.bounding_rectangle.x for band in self.bands]

        # calculating the mean difference of the x coordinates
        mean_difference, differences = self.band_distance_differences(x_list)

        # if 2 x coordinates are less than 0.4 x the mean difference away from each other, assume it is a duplicate band
        for index in range(len(differences)):
            if differences[index] < mean_difference * 0.4:
                self.bands[index].dupe = True
                self.bands[index + 1].dupe = True

    def band_distance_differences(self, list):
        np_list = np.array(list)
        differences = np.diff(np_list)
        mean_difference = np.mean(differences)

        return mean_difference, differences

    def keep_biggest_dupe_band(self):

        for band in self.bands:
            if band.colour == 'GOLD' and band.dupe is True:
                band.dupe = False
                print("GOLD DUPE")

        areas = []

        for band in self.bands:
            if band.dupe is True:
                area = band.bounding_rectangle.width * band.bounding_rectangle.height
                areas.append(area)

        if areas:
            # I am assuming that the best colour match is the best band
            biggest_area = max(areas)
            biggest_area_index = areas.index(biggest_area)

            for band in self.bands[:]:
                if self.bands.index(band) != biggest_area_index:
                    self.bands.remove(band)

    def best_match(self):
        pass

    def find_gold(self):

        gold_x_list = [band.bounding_rectangle.x for band in self.bands if band.colour == 'GOLD']
        x_list = [band.bounding_rectangle.x for band in self.bands if band.colour != 'GOLD']

        mean_difference, difference_list = self.band_distance_differences(x_list)

        gold_x_false_positives = []

        for x in x_list:
            for gold_x in gold_x_list:
                if (x + (mean_difference * 0.7)) < gold_x < (x - (mean_difference * 0.7)):
                    gold_x_false_positives.append(gold_x)

        for band in self.bands[:]:
            if band.bounding_rectangle.x in gold_x_false_positives:
                self.bands.remove(band)

    def main(self):

        self.remove_non_bands()
        #self.find_gold()
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
