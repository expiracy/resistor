from detection.ResistorBand import ResistorBand


class BandIdentifier:
    def __init__(self, possible_bands, slice_bands):
        self.possible_bands = possible_bands
        self.slice_bands = slice_bands

    # Finding the most frequent bands.
    def find_most_frequent_bands(self):

        resistor_band_colours = []

        for band_number, possible_colours in self.possible_bands.items():
            band_colour = max(set(possible_colours), key=possible_colours.count)

            resistor_band_colours.append(band_colour)

        return resistor_band_colours

    # Create instances of ResistorBand, that are to make up Resistor.
    def create_resistor_bands(self, resistor_band_colours):

        resistor_bands = []

        for resistor_band_colour in resistor_band_colours:
            resistor_band = ResistorBand(resistor_band_colour)
            resistor_bands.append(resistor_band)

        return resistor_bands

    # Finding the resistor bands with the most frequent bands or alternate criteria.
    def find_resistor_bands(self):
        try:
            resistor_band_colours = self.find_most_frequent_bands()

            if not resistor_band_colours:
                resistor_band_colours = self.slice_bands[len(self.slice_bands) // 2]

            resistor_bands = self.create_resistor_bands(resistor_band_colours)

            return resistor_bands

        except Exception as E:
            print(E)

            return None
