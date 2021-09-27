import os
from enum import Enum
from detection.ResistorBand import ResistorBand

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

from detection.Colour import Colour

from detection.HSVRange import HSVRange


class Colours:

    def __init__(self):
        pass

    def lookup_hsv_range(self, colour):
        h_ranges = {
            'BLACK': [0, 180],
            'BROWN': [0, 15],
            'RED': [150, 180],
            'ORANGE': [5, 15],
            'YELLOW': [20, 70],
            'GREEN': [40, 80],
            'BLUE': [90, 140],
            'VIOLET': [120, 160],
            'GREY': [0, 0],
            'WHITE': [0, 180],
            'GOLD': [10, 23],
            'SILVER': [0, 0],
        }

        s_ranges = {
            'BLACK': [0, 255],
            'BROWN': [40, 120],
            'RED': [60, 200],
            'ORANGE': [100, 180],
            'YELLOW': [100, 255],
            'GREEN': [100, 255],
            'BLUE': [150, 255],
            'VIOLET': [30, 140],
            'GREY': [0, 0],
            'WHITE': [0, 30],
            'GOLD': [70, 100],
            'SILVER': [0, 1],
        }

        v_ranges = {
            'BLACK': [0, 50],
            'BROWN': [40, 80],
            'RED': [60, 110],
            'ORANGE': [80, 140],
            'YELLOW': [100, 255],
            'GREEN': [0, 255],
            'BLUE': [0, 130],
            'VIOLET': [40, 120],
            'GREY': [40, 130],
            'WHITE': [127, 255],
            'GOLD': [20, 70],
            'SILVER': [80, 130],
        }

        return HSVRange(h_ranges[colour], s_ranges[colour], v_ranges[colour])


