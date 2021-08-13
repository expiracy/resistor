import os
from enum import Enum
from detection.ResistorBands import ResistorBands

from detection.Color import Color


class Colors:
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
        return Colors()

    def __init__(self):

        self.colors = []
        self.load_colors("../detection/data/colors.dat")
        self.detected_colors = []

    def load_colors(self, location):

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

                color = Color(name, red, green, blue)

                self.colors.append(color)

    def find(self, bgr):

        colors = self.colors.copy()

        colors = sorted(colors, key=lambda color: color.distance(bgr))

        nearest = colors[0]

        return self.enumeration(nearest)

    def enumeration(self, name):

        for color in self.Name:
            if color.name in str(name).upper():
                return color.name

        return self.Name.UNKNOWN

    def display(self, colors):

        for index in range(len(colors)):
            color = colors[index]
            print(color)

            self.detected_colors.append(color)

        return self



