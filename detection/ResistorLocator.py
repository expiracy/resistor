import math
import os
import random

import cv2

import numpy as np

from detection.Image import Image
from detection.BandLocator import BandLocator
from detection.Greyscale import Greyscale
from detection.Annotation import Annotation
from detection.BGR import BGR


class ResistorLocator:

    def __init__(self, image):
        self.image = image

    # From https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    def extract_resistor(self, rectangle):
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)

        # get width and height of the detected rectangle
        width = int(rectangle[1][0])
        height = int(rectangle[1][1])

        src_pts = box.astype("float32")

        # coordinate of the points in box points after the rectangle has been
        # straightened
        dst_pts = np.array([[0, height - 1],
                            [0, 0],
                            [width - 1, 0],
                            [width - 1, height - 1]], dtype="float32")

        # the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # directly warp the rotated rectangle to get the straightened rectangle
        self.image = self.image.warp_perspective(matrix, width, height)

        if self.image.width() > self.image.height():
            self.image = self.image.rotate(90)

        return self.image

    def find_resistor_contour(self):
        greyscale_image = Greyscale(self.image.image, "BGR")

        monochrome_image = greyscale_image.monochrome(inverted=True)

        contours, _ = monochrome_image.find_contours()

        # Fill in the holes in the resistor area so we can safely erode the image later
        # Erode the wires away - the ksize needs to be bigger than wires and smaller than resistor body
        eroded_image = Annotation(monochrome_image.image).draw_contours(contours).erode()

        # Now the biggest contour should only be the resistor body
        contours, _ = Greyscale(eroded_image.image).find_contours()

        # Sort the contours so  the biggest contour is first
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get the first (biggest) contour
        resistor_body_contour = sorted_contours[0]

        return resistor_body_contour

    def locate(self):
        resistor_body_contour = self.find_resistor_contour()

        # This should  wrap a box with the correct orientation around the resistor body
        minimum_rectangle = cv2.minAreaRect(resistor_body_contour)

        resistor_image = self.extract_resistor(minimum_rectangle)

        return resistor_image


if __name__ == '__main__':
    os.chdir("../..")

    directory = os.path.abspath(os.curdir)

    folder = f'{directory}\\resistor\\images'

    image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\\images\\BROWN BLACK BROWN GOLD (2).JPG')

    image = Image(image)
    resistor_image = ResistorLocator(image).locate()
    # BandLocator(resistor_image)
    resistor_image.show()
