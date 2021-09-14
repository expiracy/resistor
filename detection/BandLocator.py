import cv2
import numpy
import numpy as np

import os
import glob

from detection.HSV import HSV

from detection.Colours import Colours
from detection.Image import Image
from detection.ResistorBand import ResistorBand
from detection.Resistor import Resistor
from detection.BoundingRectangle import BoundingRectangle
from detection.Greyscale import Greyscale
from detection.BGR import BGR


class BandLocator:

    def __init__(self, image):
        self.image = image

    def remove_outlier_contours(self, contours):

        bounding_rectangles = []

        for contour in contours:
            bounding_rectangle = BoundingRectangle(contour)

            bounding_rectangles.append(bounding_rectangle)

        areas = [bounding_rectangle.width * bounding_rectangle.height for bounding_rectangle in bounding_rectangles]

        mean = np.mean(areas)

        lower_bound = mean - (mean * 0.6)

        # write about different outlier algorithms tried

        outlier_indexes = []

        for index in range(len(areas))[:]:
            if areas[index] < lower_bound:
                contours.remove(contours[index])

        return contours

    def threshold(self):

        blurred_image = self.image.clone().blur(1, round(self.image.height() * 0.2))

        blurred_image.show()

        monochrome_image = blurred_image.clone().monochrome()

        contours, _ = monochrome_image.contours()

        contours_image = blurred_image.clone().contours(contours).show()

        return contours

    def slice_resistor(self):

        slices = []

        for slice in range(self.image.height()):
            x = 0

            slice = self.image.clone().region(x, slice, self.image.width(), 1)

            slice.show()

            slices.append(slice)

        return slices

    def locate(self):

        self.image = self.image.resize(self.image.width(), self.image.height() * 5)

        blurred_image = BGR(self.image.image).blur()

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD',
                   'SILVER']

        resistor_bands = []

        for colour in colours:

            hsv_ranges = Colours().lookup_hsv_range(colour)

            band_contours = None

            if colour == 'GOLD':

                #band_contours = self.threshold()
                pass

            else:

                slices = self.slice_resistor()

                for slice in slices:
                    slice.show()



                hsv_image = HSV(blurred_image.image, 'BGR')
                colour_mask = hsv_image.mask(hsv_ranges)

                #print(colour)
                #colour_mask.show()

                greyscale_mask_image = Greyscale(colour_mask, 'HSV')

                print(colour)

                non_zero_pixels = greyscale_mask_image.count_non_zero_pixels()

                if non_zero_pixels != 0:
                    band_contours, _ = greyscale_mask_image.find_contours()

            if band_contours is not None:

                for contour in band_contours:
                    bounding_rectangles = BoundingRectangle(contour)

                    resistor_band = ResistorBand(colour, bounding_rectangles)

                    resistor_bands.append(resistor_band)

            #self.image.blur().show()

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
