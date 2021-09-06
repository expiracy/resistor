import cv2
import numpy
import numpy as np

import os
import glob

from detection.Colours import Colours
from detection.Image import Image
from detection.ResistorBand import ResistorBand
from detection.Resistor import Resistor
from detection.BoundingRectangle import BoundingRectangle


class BandLocator:

    def __init__(self, image):
        self.image = image

    def remove_outlier_contours(self, contours):

        bounding_rectangles = []

        for contour in contours:
            bounding_rectangle = BoundingRectangle(contour)

            bounding_rectangles.append(bounding_rectangle)

        areas = []

        for index in range(len(bounding_rectangles)):
            areas.append(bounding_rectangles[index].width * bounding_rectangles[index].height)

        mean = np.mean(areas)

        lower_bound = mean - (mean * 0.6)

        # write about different outlier algorithms tried

        outlier_indexes = []

        for index in range(len(areas)):
            if areas[index] < lower_bound:
                outlier_indexes.append(index)

        for index in outlier_indexes:
            contours.remove(contours[index])

        return contours

    def find_gold(self):

        blurred_image = self.image.clone().blur(1, round(self.image.height() * 0.7))

        monochrome_image = blurred_image.clone().monochrome(inverted=True, block_size=151, C=1)

        contours, _ = monochrome_image.contours()

        # contours_image = self.image.draw_contours(contours)

        return contours

    def locate(self):

        self.image = self.image.region(round(self.image.width() * 0.04), 0, round(self.image.width() * 0.92),
                                       self.image.height() * 2).resize(self.image.width(), self.image.height() * 5)

        blurred_image = self.image.blur()

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD',
                   'SILVER']

        resistor_bands = []

        for colour in colours:

            colour_hsv_ranges = Colours().lookup_hsv_range(colour)

            band_contours = None

            #if colour == 'GOLD':

                #band_contours = self.find_gold()

            colour_mask = blurred_image.hsv_mask(colour_hsv_ranges)

            non_zero_pixels = colour_mask.count_non_zero_pixels()

            if non_zero_pixels != 0:
                band_contours, _ = colour_mask.contours()

            if band_contours is not None:

                for contour in band_contours:
                    bounding_rectangles = BoundingRectangle(contour)

                    resistor_band = ResistorBand(colour, bounding_rectangles)

                    resistor_bands.append(resistor_band)

        return resistor_bands


if __name__ == "__main__":
    directory = os.path.abspath(os.curdir)
    ''''
    folder = f'{directory}\\resistorImages'

    for filename in os.listdir(folder):
        if filename.endswith('jpg'):
            resistor_image = cv2.imread(f'{folder}\\{filename}')
            
    '''
    resistor_image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\detection\\resistorImages\\269661054352669044576758484705730405017.jpg')
    resistor_image = Image(resistor_image)

    BandLocator(resistor_image).locate()
