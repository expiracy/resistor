from detection.Colour import Colour
from detection.HSVRange import HSVRange


# Class that contains all the hsv ranges for every resistor colour.
class HSVRanges:
    def __init__(self):
        self.hsv_ranges = {
            Colour.UNKNOWN: HSVRange([255, 255], [255, 255], [255, 255]),
            Colour.BLACK: HSVRange([0, 255], [0, 255], [0, 30]),
            Colour.BROWN: HSVRange([170, 10], [100, 190], [20, 75]),
            Colour.RED: HSVRange([175, 5], [100, 255], [50, 150]),
            Colour.ORANGE: HSVRange([5, 15], [100, 255], [70, 130]),
            Colour.YELLOW: HSVRange([20, 30], [100, 255], [80, 130]),
            Colour.GREEN: HSVRange([40, 75], [100, 255], [40, 90]),
            Colour.BLUE: HSVRange([100, 115], [100, 255], [40, 80]),
            Colour.VIOLET: HSVRange([135, 170], [70, 255], [35, 85]),
            Colour.GREY: HSVRange([0, 255], [0, 20], [50, 75]),
            Colour.WHITE: HSVRange([0, 20], [10, 40], [110, 255]),
            Colour.GOLD: HSVRange([10, 25], [70, 150], [30, 70]),
            Colour.SILVER: HSVRange([0, 1], [0, 1], [80, 130]),
        }

    def for_colour(self, colour):
        return self.hsv_ranges[colour]
