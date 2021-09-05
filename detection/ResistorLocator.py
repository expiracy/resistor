import math
import os
import random

import cv2

import numpy as np

from detection.Image import Image
from detection.BandLocator import BandLocator


class ResistorLocator:

    def __init__(self, image):
        self.image = image

    # From https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    def extract_rotated_rectangle(self, rectangle):
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
        warped_image = cv2.warpPerspective(self.image.image, matrix, (width, height))

        if warped_image.shape[0] > warped_image.shape[1]:
            warped_image = cv2.rotate(warped_image, cv2.ROTATE_90_CLOCKWISE)

        return Image(warped_image)

    def extract_resistor(self):

        monochrome_image = self.image.monochrome(inverted=True)

        contours, _ = monochrome_image.contours()

        # Fill in the holes in the resistor area so we can safely erode the image later
        contour_image = monochrome_image.draw_contours(contours)

        # Erode the wires away - the ksize needs to be bigger than wires and smaller than resistor body
        eroded_image = contour_image.erode()

        # Now the biggest contour should only be the resistor body
        contours, _ = eroded_image.contours()

        # Sort the contours so  the biggest contour is first
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get the first (biggest) contour
        biggest_contour = sorted_contours[0]

        # This should  wrap a box with the correct orientation around the resistor body
        minimum_rectangle = cv2.minAreaRect(biggest_contour)

        resistor_image = self.extract_rotated_rectangle(minimum_rectangle)

        return resistor_image

    def locate(self):
        resistor_image = self.extract_resistor()

        return resistor_image


if __name__ == '__main__':

    os.chdir("../..")

    directory = os.path.abspath(os.curdir)

    folder = f'{directory}\\resistor\\images'

    for filename in os.listdir(folder):
        print(filename)

        image = cv2.imread(f'{folder}\\{filename}')

        if filename.endswith('JPG'):
            image = Image(image)
            resistor_image = ResistorLocator(image).locate()
            #BandLocator(resistor_image)
            resistor_image.show()

