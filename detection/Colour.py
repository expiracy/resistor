from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

class Colour:

    def __init__(self, h, s, v):

        self.rgb = self.HSV_to_RGB(h, s, v)
        self.lab = convert_color(self.rgb, LabColor)

    def HSV_to_RGB(self, h, s, v):

        # sRGBColor(red, green, blue, is_upscaled=True)
        pass

    def distance(self, bgr):

        red = bgr[2]
        green = bgr[1]
        blue = bgr[0]

        rgb = sRGBColor(red, green, blue, is_upscaled=True)
        lab = convert_color(rgb, LabColor)

        return delta_e_cie2000(lab, self.lab)

