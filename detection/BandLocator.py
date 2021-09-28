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
from detection.SliceBands import SliceBands
from detection.SliceBand import SliceBand


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

        height = self.image.height()

        slice_height = round(height * 0.05)

        slice_amount = height // slice_height

        image_slices = []

        for slice_number in range(slice_amount):
            x = 0
            y = slice_number * slice_height

            image_slice = self.image.clone().region(x, y, self.image.width(), slice_height)

            image_slices.append(image_slice)

        return image_slices

    def bands(self, image_slice):

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD',
                   'SILVER']

        bands = []

        for colour in colours:

            hsv_ranges = Colours().lookup_hsv_range(colour)

            hsv_image = HSV(image_slice.image, 'BGR')
            colour_mask = hsv_image.mask(hsv_ranges)

            greyscale_mask_image = Greyscale(colour_mask, 'HSV')

            non_zero_pixels = greyscale_mask_image.count_non_zero_pixels()

            band_contours = None

            if non_zero_pixels != 0:
                band_contours, _ = greyscale_mask_image.find_contours()

            if band_contours is not None:
                print(colour)
                greyscale_mask_image.show()

                for contour in band_contours:
                    bounding_rectangles = BoundingRectangle(contour)

                    band = SliceBand(colour, bounding_rectangles)

                    bands.append(band)

        return bands

    def locate(self):

        self.image = self.image.resize(self.image.width(), self.image.height() * 50)
        self.image = BGR(self.image.image).blur(1, round(self.image.height() * 0.5))
        #self.image = BGR(self.image.image).bilateral_filter()

        cv2.imshow("image", self.image.image)
        self.image.show()

        image_slices = self.slice_resistor()

        slice_bands = []

        for image_slice in image_slices:
            bands_for_slice = self.bands(image_slice)

            slice_bands.append(bands_for_slice)

        SliceBands(slice_bands).find_resistor_bands()

        # resistor = Resistor(bands_for_slice).main()

        # print(resistor.colours())


if __name__ == "__main__":
    directory = os.path.abspath(os.curdir)
    ''''
    folder = f'{directory}\\resistorImages'

    for filename in os.listdir(folder):
        if filename.endswith('jpg'):
            resistor_image = cv2.imread(f'{folder}\\{filename}')

    '''
    resistor_image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\detection\\resistorImages\\269661054352669044576758484705730405017.jpg')
    resistor_image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\detection\\resistorImages\\272317250836272132017112746513351615129.jpg')
    #resistor_image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\detection\\resistorImages\\52114446105322085404135713747236856473.jpg')
    resistor_image = Image(resistor_image)

    BandLocator(resistor_image).locate()