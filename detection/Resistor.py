class Resistor:

    def __init__(self):
        self.bands = []
        self.type = 6

    @classmethod
    def create(cls):
        return Resistor()

    def identify_type(self, bands):

        self.type = len(bands)

    def bands_for_type(self):

        if self.type == 3:
            self.bands = [self.bands[0], self.bands[1], "NONE", self.bands[2], "NONE", "NONE"]

        if self.type == 4:
            self.bands = [self.bands[0], self.bands[1], "NONE", self.bands[2], self.bands[3], "NONE"]

        if self.type == 5:
            self.bands = [self.bands[0], self.bands[1], self.bands[2], self.bands[3], self.bands[4], "NONE"]









