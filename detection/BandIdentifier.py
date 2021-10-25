import numpy as np


class BandIdentifier:
    def __init__(self, possible_bands, slice_bands):
        self.possible_bands = possible_bands
        self.slice_bands = slice_bands
        self.bands = []

    def find_most_frequent_bands(self):
        try:
            resistor_bands = []

            for index in range(len(self.possible_bands[0])):
                band_colours = [bands[index] for bands in self.possible_bands]

                band_colour = max(set(band_colours), key=band_colours.count)

                resistor_bands.append(band_colour)

        except:
            print("Error with input list.")

            resistor_bands = None

        return resistor_bands

    def find_resistor_bands(self, number_of_bands):
        try:
            resistor_bands = self.find_most_frequent_bands()

            if resistor_bands is None:
                for slice_number in self.slice_bands:
                    if len(slice_number) == number_of_bands:
                        resistor_bands = [band.colour for band in self.slice_bands[self.slice_bands.index(slice_number)]]

                print("Alternate band finding method used.")

            return resistor_bands

        except ValueError:
            print("Error with BandIdentifier.")

