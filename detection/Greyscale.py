import cv2
import numpy as np

from detection.Image import Image
from detection.BGR import BGR

class Greyscale(Image):

    def __init__(self, image=None, type='GREYSCALE'):
        greyscale = self.greyscale_conversion(image, type)
        super().__init__(greyscale)

    # Finds contours of an image.
    def find_contours(self):

        contours, hierarchy = cv2.findContours(self.image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        return contours, hierarchy

    # Returns the number of non zero pixels.
    def count_non_zero_pixels(self):
        return cv2.countNonZero(self.image)

    # Converts an image to monochrome.
    def monochrome(self, inverted=False, block_size=51, C=21):
        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        self.image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding, block_size, C)

        return self

    # Conversion between types.
    def greyscale_conversion(self, image, type):
        if type == 'BGR':
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if type == 'HSV':
            return image

        if type == 'HSV':
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if type == 'GREYSCALE':
            return image

