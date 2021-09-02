class ResistorBand:

    def __init__(self, colour, contours):
        self.colours = []
        self.amount = 6
        self.colour = colour
        self.contours = contours

    def identify_type(self, bands):

        self.amount = len(bands)

    def bands_for_type(self):

        if self.amount == 3:
            self.colours = [self.colours[0], self.colours[1], "NONE", self.colours[2], "NONE", "NONE"]

        if self.amount == 4:
            self.colours = [self.colours[0], self.colours[1], "NONE", self.colours[2], self.colours[3], "NONE"]

        if self.amount == 5:
            self.colours = [self.colours[0], self.colours[1], self.colours[2], self.colours[3], self.colours[4], "NONE"]









