import os
from enum import Enum
from detection.ResistorBands import ResistorBands

from detection.Colour import Colour


class Colours:
    class Name(Enum):

        # to return only the name of the enum
        def __str__(self):
            return str(self.name)

        BLACK = 0,
        BROWN = 1,
        RED = 2,
        ORANGE = 3,
        YELLOW = 4,
        GREEN = 5,
        BLUE = 6,
        VIOLET = 7,
        GREY = 8,
        WHITE = 9,
        SILVER = 10,
        GOLD = 11,
        UNKNOWN = 13

    @classmethod
    def create(cls):
        return Colours()

    def __init__(self):

        self.colours = []
        self.load_colours("../detection/data/colors.dat")
        self.detected_colours = []

    def load_colours(self, location):

        print(os.path.abspath(location))

        with open(location) as file:
            for line in file.readlines():

                if "!" in line:
                    continue

                elements = line.split()

                if len(elements) == 0:
                    continue

                red = int(elements[0])
                green = int(elements[1])
                blue = int(elements[2])
                name = elements[3]

                colour = Colour(name, red, green, blue)

                self.colours.append(colour)

    def find(self, bgr):

        colours = self.colours.copy()

        colours = sorted(colours, key=lambda colour: colour.distance(bgr))

        nearest = colours[0]

        return self.enumeration(nearest)

    def enumeration(self, name):

        for colour in self.Name:
            if colour.name in str(name).upper():
                return colour.name

        return self.Name.UNKNOWN

    def display(self, colours):

        for index in range(len(colours)):
            colour = colours[index]
            print(colour)

            self.detected_colors.append(colour)

        return self



