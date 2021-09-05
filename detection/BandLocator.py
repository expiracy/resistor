import cv2 as cv2
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

    def remove_outlier_rectangles(self, rectangles):

        areas = []

        for index in range(len(rectangles)):

            areas.append(rectangles[index].width * rectangles[index].height)

        mean = np.mean(areas)

        lower_bound = mean - (mean * 0.6)

        outliers = []

        # write about different outlier algorithms tried

        for index in range(len(areas)):

            if areas[index] < lower_bound:

                outliers.append(rectangles[index])

        for outlier in outliers:

            rectangles.remove(outlier)

        return rectangles

    def locate(self):

        trimmed_image = self.image.clone().region(round(self.image.width() * 0.04), 0, round(self.image.width() * 0.92),
                                                  self.image.height() * 2)

        resized_image = trimmed_image.clone().resize(trimmed_image.width(), trimmed_image.height() * 5)

        blurred_image = resized_image.clone().blur(1, round(resized_image.height()))

        #blurred_image.show()

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD',
                   'SILVER']

        resistor_bands = []

        for colour in colours:

            hsv_ranges = Colours().lookup_hsv_range(colour)

            if colour == 'GOLD':
                band_contours = resized_image.hsv_mask(hsv_ranges)

            else:
                band_contours = blurred_image.hsv_mask(hsv_ranges)

            if band_contours is not None:

                for contour in band_contours:

                    bounding_rectangle = BoundingRectangle(contour)

                    resistor_band = ResistorBand(colour, bounding_rectangle)

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



