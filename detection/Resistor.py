class Resistor:

    def __init__(self):
        self.bands = []
        self.type = 6
        self.ohms = 0

    @classmethod
    def create(cls):
        return Resistor()

    def findType(self, bands):
        self.type = len(bands)

        return self.type

    def findBands(self, detected_colors):
        detected_colors.remove("BROWN")
        self.bands = detected_colors

        return self.bands

