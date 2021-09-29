from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

import colorsys

class Colour:

    def __init__(self):
        pass

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

    def rgb_to_hsv(self, r, g, b):

        # R, G, B values are divided by 255
        # to change the range from 0..255 to 0..1:
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        # h, s, v = hue, saturation, value
        cmax = max(r, g, b)  # maximum of r, g, b
        cmin = min(r, g, b)  # minimum of r, g, b
        diff = cmax - cmin  # diff of cmax and cmin.

        # if cmax and cmax are equal then h = 0
        if cmax == cmin:
            h = 0

        # if cmax equal r then compute h
        elif cmax == r:
            h = (60 * ((g - b) / diff) + 360) % 360

        # if cmax equal g then compute h
        elif cmax == g:
            h = (60 * ((b - r) / diff) + 120) % 360

        # if cmax equal b then compute h
        elif cmax == b:
            h = (60 * ((r - g) / diff) + 240) % 360

        # if cmax equal zero
        if cmax == 0:
            s = 0
        else:
            s = (diff / cmax) * 255

        # compute v
        v = cmax * 255

        h /= 2

        return h, s, v


