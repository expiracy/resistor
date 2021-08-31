import math
import os
import random

import cv2

import numpy as np

from Image import Image


class ResistorLocator:

    def __init__(self):
        pass

    # From https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    def extract_rotated_rectangle(self, img, rect):
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # get width and height of the detected rectangle
        width = int(rect[1][0])
        height = int(rect[1][1])

        src_pts = box.astype("float32")

        # coordinate of the points in box points after the rectangle has been
        # straightened
        dst_pts = np.array([[0, height - 1],
                            [0, 0],
                            [width - 1, 0],
                            [width - 1, height - 1]], dtype="float32")

        # the perspective transformation matrix
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # directly warp the rotated rectangle to get the straightened rectangle
        warped = cv2.warpPerspective(img, M, (width, height))

        if warped.shape[0] > warped.shape[1]:
            warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)

        return warped

    def extract_resistor(self, image):
        image = Image(image)

        monochrome_image = image.monochrome(inverted=True)

        contours, _ = monochrome_image.contours()

        # Fill in the holes in the resistor area so we can safely erode the image later
        contour_image = monochrome_image.draw_contours(contours)

        # Erode the wires away - the ksize needs to be bigger than wires and smaller than resistor body
        eroded_image = contour_image.erode()

        # Now the biggest contour should only be the resistor body
        contours, _ = eroded_image.contours()

        # Sort the contours so  the biggest contour is first
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get the first (biggest) contour
        contour = contours[0]

        # This should  wrap a box with the correct orientation around the resistor body
        rectangle = cv2.minAreaRect(contour)

        image = self.extract_rotated_rectangle(image.image, rectangle)

        cv2.destroyAllWindows()

        return image

    def locate(self, filename):
        image = cv2.imread(filename)

        resistor_image = self.extract_resistor(image)

        return Image(resistor_image)


if __name__ == '__main__':

    os.chdir("../..")

    directory = os.path.abspath(os.curdir)

    folder = f'{directory}\\resistor\\images'

    for filename in os.listdir(folder):

        resistor_locator = ResistorLocator()

        print(filename)

        if filename.endswith('JPG'):
            resistor_image = resistor_locator.locate(f'{folder}\\{filename}')
