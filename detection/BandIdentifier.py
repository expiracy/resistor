import numpy as np


class BandIdentifier:
    def __init__(self, possible_bands, slice_bands):
        self.possible_bands = possible_bands
        self.slice_bands = slice_bands
        self.bands = []

    # Finding the most frequent bands.
    def find_most_frequent_bands(self):
        try:
            resistor_bands = []

            for index in range(len(self.possible_bands[0])):
                band_colours = [bands[index] for bands in self.possible_bands]

                band_colour = max(set(band_colours), key=band_colours.count)

                resistor_bands.append(band_colour)

        except Exception as E:
            print('Error with input list.')
            print(E)

            resistor_bands = None

        return resistor_bands

    # Finding the resistor bands with the most frequent bands or alternate criteria.
    def find_resistor_bands(self, number_of_bands):
        try:
            resistor_bands = self.find_most_frequent_bands()

            if not resistor_bands:
                while resistor_bands is None:
                    for slice_number in self.slice_bands:
                        if len(slice_number) == number_of_bands:
                            resistor_bands = [band.colour for band in
                                              self.slice_bands[self.slice_bands.index(slice_number)]]
                            return resistor_bands

                    number_of_bands -= 1

                    if number_of_bands == 0:
                        return None

            else:
                return resistor_bands

        except Exception as E:
            print('Error with BandIdentifier.')
            print(E)
