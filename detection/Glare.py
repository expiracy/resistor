import cv2
from detection.BoundingRectangle import BoundingRectangle
from detection.Greyscale import Greyscale
from detection.BGR import BGR
from detection.HSV import HSV
from detection.HSVRange import HSVRange
from detection.BoundingRectangle import BoundingRectangle

import numpy as np

class Glare:
    def __init__(self, image):
        self.image = image

    def locate(self):
        self.image = self.image.resize(self.image.width(), self.image.height() * 10)

        self.image = BGR(self.image.image).blur(round(self.image.width() * 5), 1)

        h_range = [10, 20]
        s_range = [10, 60]
        v_range = [110, 130]

        glare_mask = HSV(self.image.image, 'BGR').mask(HSVRange(h_range, s_range, v_range))
        greyscale_glare_mask = Greyscale(glare_mask, 'HSV')

        glare_contours, _ = greyscale_glare_mask.find_contours()

        for glare_contour in glare_contours:
            glare_bounding_rectangle = BoundingRectangle(glare_contour)

            max_glare_y = glare_bounding_rectangle.y + glare_bounding_rectangle.height

            self.image.image = self.image.image[glare_bounding_rectangle.y, max_glare_y]

            self.image.show()




        self.image.show()

        greyscale_glare_mask.show()

        return True