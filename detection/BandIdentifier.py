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

    def find_resistor_bands(self):
        try:
            resistor_bands = self.find_most_frequent_bands()

            if resistor_bands is None:
                resistor_bands = [band.colour for band in self.slice_bands[len(self.slice_bands) // 2]]

            return resistor_bands

        except:
            print("Error with BandIdentifier.")

