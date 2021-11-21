from detection.Colour import Colour
from detection.ResistorBand import ResistorBand


# Initiates with the possible bands and the full list of slice bands. Finds the resistor bands from the initiated data.
class BandIdentifier:
    def __init__(self, possible_bands):
        self.possible_bands = possible_bands
        self.colour_weights = {
            Colour.UNKNOWN: 0,
            Colour.BLACK: 0.5,
            Colour.BROWN: 1,
            Colour.RED: 1,
            Colour.ORANGE: 0.75,
            Colour.YELLOW: 1,
            Colour.GREEN: 1,
            Colour.BLUE: 1,
            Colour.VIOLET: 1,
            Colour.GREY: 1,
            Colour.WHITE: 0.5,
            Colour.GOLD: 1,
            Colour.SILVER: 0.75,
        }

    def find_band_colour_counts(self):
        try:
            slice_band_groups = self.possible_bands.groups()

            band_colour_counts = []

            for index, _ in enumerate(slice_band_groups):
                band_colour_counts.append({})

            for index, slice_band_groups in enumerate(slice_band_groups):

                color_counts = band_colour_counts[index]

                if slice_band_groups:

                    for slice_band in slice_band_groups:
                        colour = slice_band.colour

                        count = color_counts.get(colour, 0)

                        color_counts[colour] = count + 1
                else:
                    color_counts[Colour.UNKNOWN] = 1

            return band_colour_counts

        except Exception as error:
            raise Exception(f'Error counting number of possible bands, {error}')

    def apply_colour_weights(self, band_colour_counts):
        try:
            for index, colour_counts in enumerate(band_colour_counts):

                for colour, count in colour_counts.items():

                    weight = self.colour_weights[colour]

                    if colour is Colour.GOLD or colour is Colour.SILVER:
                        if index == 0 or index == len(band_colour_counts) - 1:
                            weight *= 2
                        else:
                            weight /= 2

                    colour_counts[colour] = weight * count

            return band_colour_counts

        except Exception as error:
            raise Exception(f'Error applying colour weights, {error}')

    def find_most_frequent_bands(self, band_colour_counts):
        try:
            resistor_bands = []

            for colour_counts in band_colour_counts:
                colour = max(colour_counts, key=colour_counts.get)

                resistor_bands.append(ResistorBand(colour))

            return resistor_bands

        except Exception as error:
            raise Exception(f'Error finding most frequent bands, {error}')

    # Finding the resistor bands with the most frequent bands or alternate criteria.
    def find_resistor_bands(self):
        try:
            band_colour_counts = self.find_band_colour_counts()

            band_colour_counts = self.apply_colour_weights(band_colour_counts)

            resistor_bands = self.find_most_frequent_bands(band_colour_counts)

            return resistor_bands

        except Exception as error:
            raise Exception(f'Error identifying resistor bands: {error}')
