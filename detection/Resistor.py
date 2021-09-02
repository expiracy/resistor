class Resistor:
    def __init__(self, resistor_bands):
        self.resistor_bands = resistor_bands

    def main(self):
        self.remove_non_bands()

    def find_band_order(self):
        pass

    def remove_non_bands(self):
        for index in range(len(self.resistor_bands)):
            pass