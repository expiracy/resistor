from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

class Colour:

    def __init__(self, name, red, green, blue):
        self.name = name

        self.rgb = sRGBColor(red, green, blue, is_upscaled=True)
        self.lab = convert_color(self.rgb, LabColor)

    def distance(self, bgr):

        red = bgr[2]
        green = bgr[1]
        blue = bgr[0]

        rgb = sRGBColor(red, green, blue, is_upscaled=True)
        lab = convert_color(rgb, LabColor)

        return delta_e_cie2000(lab, self.lab)

    def __str__(self):
        return str(self.name)

