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

    # Returns the formatted colours for the resistor.
    def colours(self):
        type = self.type()

        if type == 3:
            colours = [self.bands[0], self.bands[1], None, self.bands[2], None, None]

        elif type == 4:
            colours = [self.bands[0], self.bands[1], None, self.bands[2],
                       self.bands[3], None]

        elif type == 5:
            colours = [self.bands[0], self.bands[1], self.bands[2], self.bands[3],
                       self.bands[4], None]

        elif type == 6:
            colours = [self.bands[0], self.bands[1], self.bands[2], self.bands[3],
                       self.bands[4], self.bands[5]]
        else:
            colours = [None, None, None, None, None, None]

        return colours

    # Gets the digit band colours.
    def get_digit_band_colours(self, colours):
        digit_band_colours = []

        if colours:
            for index in range(3):
                if colours[index] is not None:
                    digit_band_colours.append(colours[index])

            return digit_band_colours

    # Checks if the resistor digit band colours are in the standard values database.
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

        except ValueError:
            print("Error with Resistor.")

            return self
