import json
import os


class Resistor:
    def __init__(self, bands):
        self.bands = bands
        self.valid = False

    # Returns the resistor type.
    def type(self):
        if self.bands:

            type = len(self.bands)

            non_band_count = 0

            for band in self.bands:
                if band is None:
                    non_band_count += 1

            type = type - non_band_count

            return type

        else:
            return 6

    # Returns the formatted bands for the resistor.
    def colours(self):
        type = self.type()

        if type == 3:
            colours = [self.bands[0].colour, self.bands[1].colour, None, self.bands[2].colour, None, None]

        elif type == 4:
            colours = [self.bands[0].colour, self.bands[1].colour, None, self.bands[2].colour,
                       self.bands[3].colour, None]

        elif type == 5:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, None]

        elif type == 6:
            colours = [self.bands[0].colour, self.bands[1].colour, self.bands[2].colour, self.bands[3].colour,
                       self.bands[4].colour, self.bands[5].colour]
        else:
            colours = [None, None, None, None, None, None]

        return colours

    # Gets the digit band bands.
    def get_digit_band_colours(self, bands):
        digit_band_colours = []

        if bands:
            for index in range(3):
                if bands[index] is not None:
                    digit_band_colours.append(bands[index])

            return digit_band_colours

    # Checks if the resistor digit band bands are in the standard values database.
    def check_valid(self):
        digit_band_colours = self.get_digit_band_colours(self.colours())

        if len(digit_band_colours) >= 2:
            type = self.type()

            if type < 5:
                number_of_digit_bands = 2

            else:
                number_of_digit_bands = 3

            data_file = f'standardResistorValues{number_of_digit_bands}sf.json'

            with open(f'{os.path.dirname(os.path.abspath(__file__))}\\data\\{data_file}') as valid_band_colours_list:

                valid_band_colours_list = json.load(valid_band_colours_list)

                if digit_band_colours in valid_band_colours_list:
                    return True

                else:
                    return False

        else:
            return False

    # Finds the most probable correct version of a resistor.
    def main(self):
        try:

            self.valid = self.check_valid()

            if self.valid is True:
                return self

            else:
                self.bands = self.bands[::-1]
                self.valid = self.check_valid()

                return self

        except Exception as E:
            print("Error with Resistor.")
            print(E)
